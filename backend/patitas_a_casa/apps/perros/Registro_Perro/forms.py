from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory

from .models import PerroPerdido, FotoPerroPerdido

class PerroPerdidoForm(forms.ModelForm):
    COLORES_CHOICES = [
        ('unico', 'Color único'),
        ('azul', 'Azul'),
        ('blanco', 'Blanco'),
        ('cafe', 'Café'),
        ('caniche', 'Caniche'),
        ('carbonatado', 'Carbonatado'),
        ('chocolate', 'Chocolate'),
        ('amarillo', 'Amarillo'),
        ('dorado', 'Dorado'),
        ('negro', 'Negro'),
    ]
    
    # Creamos un campo MultipleChoiceField para selección de colores
    colores_multiple = forms.MultipleChoiceField(
        choices=COLORES_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Combinación de colores"
    )
    
    # Campo para fecha y hora por separado para mejor UX
    fecha_perdida = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha en que se perdió"
    )
    
    hora_perdida = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label="Hora aproximada en que se perdió"
    )
    
    class Meta:
        model = PerroPerdido
        exclude = ['propietario', 'fecha_registro', 'estado', 'fecha_actualizacion', 'colores', 'fecha_hora_perdida']
        widgets = {
            'señas_particulares': forms.Textarea(attrs={'rows': 3}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre de tu mascota'}),
            'raza': forms.TextInput(attrs={'placeholder': 'Si es mestizo, indica "Mestizo"'}),
        }
        labels = {
            'edad_años': 'Edad (años)',
            'edad_meses': 'Edad (meses)',
            'esterilizado': '¿Está esterilizado?',
            'tiene_collar': '¿Llevaba collar?',
            'color_collar': 'Color del collar',
            'identificador': '¿Tiene algún identificador? (Chip, placa, etc.)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si estamos editando un objeto existente, inicializar el campo de colores
        if self.instance.pk and self.instance.colores:
            self.fields['colores_multiple'].initial = self.instance.colores.split(',')
        
        # Si estamos editando un objeto existente, inicializar fecha y hora
        if self.instance.pk and self.instance.fecha_hora_perdida:
            self.fields['fecha_perdida'].initial = self.instance.fecha_hora_perdida.date()
            self.fields['hora_perdida'].initial = self.instance.fecha_hora_perdida.time()
        
        # Mostrar campo de color del collar solo si tiene_collar es True
        self.fields['color_collar'].widget.attrs['class'] = 'conditional-field'
        self.fields['color_collar'].widget.attrs['data-condition-field'] = 'id_tiene_collar'
        self.fields['color_collar'].widget.attrs['data-condition-value'] = 'true'
    
    def clean(self):
        cleaned_data = super().clean()
        tiene_collar = cleaned_data.get('tiene_collar')
        color_collar = cleaned_data.get('color_collar')
        
        if tiene_collar and not color_collar:
            self.add_error('color_collar', _('Por favor, indica el color del collar.'))
        
        # Combinar fecha y hora en un solo campo
        fecha_perdida = cleaned_data.get('fecha_perdida')
        hora_perdida = cleaned_data.get('hora_perdida')
        
        if fecha_perdida and hora_perdida:
            from django.utils import timezone
            import datetime
            fecha_hora = datetime.datetime.combine(fecha_perdida, hora_perdida)
            fecha_hora = timezone.make_aware(fecha_hora)
            cleaned_data['fecha_hora_perdida'] = fecha_hora
        
        # Verificar que no haya elegido colores incompatibles
        colores_selected = cleaned_data.get('colores_multiple', [])
        if 'unico' in colores_selected and len(colores_selected) > 1:
            self.add_error('colores_multiple', _('No puedes seleccionar "Color único" junto con otros colores.'))
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Guardar los colores seleccionados como una cadena separada por comas
        colores_selected = self.cleaned_data.get('colores_multiple', [])
        instance.colores = ','.join(colores_selected)
        
        # Asignar fecha_hora_perdida
        instance.fecha_hora_perdida = self.cleaned_data.get('fecha_hora_perdida')
        
        if commit:
            instance.save()
        return instance


class FotoPerroPerdidoForm(forms.ModelForm):
    class Meta:
        model = FotoPerroPerdido
        fields = ['foto', 'es_principal']
        widgets = {
            'es_principal': forms.CheckboxInput(),
        }
        labels = {
            'es_principal': 'Establecer como foto principal',
        }
    
    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        if foto:
            # Validar tamaño de la imagen (max 10MB)
            if foto.size > 10 * 1024 * 1024:
                raise ValidationError(_('El tamaño máximo de la imagen es de 10MB.'))
                
            # Validar extensión
            ext = foto.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'gif']:
                raise ValidationError(_('Solo se permiten archivos JPG, JPEG, PNG y GIF.'))
        return foto


# Formulario para subir múltiples fotos a la vez
FotoPerroPerdidoFormSet = inlineformset_factory(
    PerroPerdido, 
    FotoPerroPerdido,
    form=FotoPerroPerdidoForm,
    extra=4,       # Número de formularios vacíos
    max_num=4,     # Número máximo de fotos
    can_delete=True
)