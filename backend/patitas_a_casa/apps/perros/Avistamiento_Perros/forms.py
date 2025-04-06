from django import forms
from .models import AvistamientoPerro

class AvistamientoAnonimoForm(forms.ModelForm):
    class Meta:
        model = AvistamientoPerro
        fields = [
            'entidad_federativa', 'municipio_alcaldia', 'codigo_postal', 
            'colonia', 'calle', 'numero_exterior', 'fecha_hora_avistamiento',
            'foto', 'raza', 'sexo', 'tamaño', 'color_dominante',
            'señas_particulares', 'identificador', 'estado_perro', 'descripcion'
        ]
        widgets = {
            'fecha_hora_avistamiento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'señas_particulares': forms.Textarea(attrs={'rows': 3}),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['foto'].required = False
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.es_anonimo = True
        if commit:
            instance.save()
        return instance

class AvistamientoPersonaForm(forms.ModelForm):
    class Meta:
        model = AvistamientoPerro
        fields = [
            'entidad_federativa', 'municipio_alcaldia', 'codigo_postal', 
            'colonia', 'calle', 'numero_exterior', 'fecha_hora_avistamiento',
            'foto', 'raza', 'sexo', 'tamaño', 'color_dominante',
            'señas_particulares', 'identificador', 'estado_perro', 
            'puede_albergar', 'descripcion'
        ]
        widgets = {
            'fecha_hora_avistamiento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'señas_particulares': forms.Textarea(attrs={'rows': 3}),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['foto'].required = False
        
    def save(self, commit=True, usuario=None):
        instance = super().save(commit=False)
        instance.es_anonimo = False
        if usuario:
            instance.reportado_por_usuario = usuario
        if commit:
            instance.save()
        return instance

class AvistamientoAlbergueForm(forms.ModelForm):
    class Meta:
        model = AvistamientoPerro
        fields = [
            'entidad_federativa', 'municipio_alcaldia', 'codigo_postal', 
            'colonia', 'calle', 'numero_exterior', 'fecha_hora_avistamiento',
            'foto', 'raza', 'sexo', 'tamaño', 'color_dominante',
            'señas_particulares', 'identificador', 'estado_perro', 'descripcion'
        ]
        widgets = {
            'fecha_hora_avistamiento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'señas_particulares': forms.Textarea(attrs={'rows': 3}),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['foto'].required = False
        
    def save(self, commit=True, albergue=None):
        instance = super().save(commit=False)
        instance.es_anonimo = False
        if albergue:
            instance.reportado_por_albergue = albergue
        if commit:
            instance.save()
        return instance