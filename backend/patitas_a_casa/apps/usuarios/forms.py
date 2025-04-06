from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Usuario, Albergue, ServicioAlbergue

class RegistroUsuarioForm(UserCreationForm):
    """
    Formulario para registrar un nuevo usuario en el sistema (autenticación base).
    """
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este correo electrónico ya está registrado. Por favor, utiliza otro.')
        return email

class PerfilPersonaForm(forms.ModelForm):
    """
    Formulario para completar el perfil de usuario como persona física.
    """
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'telefono']
        
    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        # Validar que solo contenga números
        if not telefono.isdigit():
            raise ValidationError('El número de teléfono solo debe contener dígitos.')
        # Validar longitud (ajustar según los estándares de números telefónicos en México)
        if len(telefono) < 10:
            raise ValidationError('El número de teléfono debe tener al menos 10 dígitos.')
        return telefono

class AlbergueForm(forms.ModelForm):
    """
    Formulario para completar el perfil de usuario como albergue.
    """
    servicios = forms.ModelMultipleChoiceField(
        queryset=ServicioAlbergue.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Albergue
        fields = [
            'nombre', 'telefono', 
            'entidad_federativa', 'municipio_alcaldia', 'codigo_postal',
            'calle', 'numero_exterior', 'referencias',
            'nombre_responsable', 'apellido_responsable', 'correo_responsable',
            'capacidad_actual', 'capacidad_maxima', 'servicios',
            'facebook', 'instagram', 'twitter', 'sitio_web',
            'imagen1', 'imagen2', 'imagen3', 'imagen4'
        ]
        
    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if not telefono.isdigit():
            raise ValidationError('El número de teléfono solo debe contener dígitos.')
        if len(telefono) < 10:
            raise ValidationError('El número de teléfono debe tener al menos 10 dígitos.')
        return telefono
    
    def clean_capacidad_maxima(self):
        capacidad_maxima = self.cleaned_data['capacidad_maxima']
        capacidad_actual = self.cleaned_data.get('capacidad_actual', 0)
        
        if capacidad_maxima < capacidad_actual:
            raise ValidationError('La capacidad máxima no puede ser menor que la capacidad actual.')
        
        return capacidad_maxima

class RegistroCompletoPersonaForm(UserCreationForm):
    """
    Formulario completo para registrar un usuario como persona física (incluye auth y perfil).
    """
    email = forms.EmailField(required=True)
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    telefono = forms.CharField(max_length=15)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este correo electrónico ya está registrado. Por favor, utiliza otro.')
        return email
    
    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if not telefono.isdigit():
            raise ValidationError('El número de teléfono solo debe contener dígitos.')
        if len(telefono) < 10:
            raise ValidationError('El número de teléfono debe tener al menos 10 dígitos.')
        return telefono
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            # Crear perfil de usuario persona
            Usuario.objects.create(
                usuario=user,
                nombre=self.cleaned_data['nombre'],
                apellido=self.cleaned_data['apellido'],
                telefono=self.cleaned_data['telefono']
            )
        
        return user

class RegistroCompletoAlbergueForm(UserCreationForm):
    """
    Formulario completo para registrar un usuario como albergue (incluye auth y perfil).
    """
    email = forms.EmailField(required=True)
    
    # Datos del albergue
    nombre_albergue = forms.CharField(max_length=200)
    telefono_albergue = forms.CharField(max_length=15)
    
    # Ubicación
    entidad_federativa = forms.CharField(max_length=100)
    municipio_alcaldia = forms.CharField(max_length=100)
    codigo_postal = forms.CharField(max_length=5)
    calle = forms.CharField(max_length=200)
    numero_exterior = forms.CharField(max_length=20)
    referencias = forms.CharField(required=False, widget=forms.Textarea)
    
    # Información del responsable
    nombre_responsable = forms.CharField(max_length=100)
    apellido_responsable = forms.CharField(max_length=100)
    correo_responsable = forms.EmailField()
    
    # Información del albergue
    capacidad_actual = forms.IntegerField(min_value=0)
    capacidad_maxima = forms.IntegerField(min_value=1)
    servicios = forms.ModelMultipleChoiceField(
        queryset=ServicioAlbergue.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    # Redes sociales (opcionales)
    facebook = forms.URLField(required=False)
    instagram = forms.URLField(required=False)
    twitter = forms.URLField(required=False)
    sitio_web = forms.URLField(required=False)
    
    # Imágenes (opcionales)
    imagen1 = forms.ImageField(required=False)
    imagen2 = forms.ImageField(required=False)
    imagen3 = forms.ImageField(required=False)
    imagen4 = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este correo electrónico ya está registrado. Por favor, utiliza otro.')
        return email
    
    def clean_telefono_albergue(self):
        telefono = self.cleaned_data['telefono_albergue']
        if not telefono.isdigit():
            raise ValidationError('El número de teléfono solo debe contener dígitos.')
        if len(telefono) < 10:
            raise ValidationError('El número de teléfono debe tener al menos 10 dígitos.')
        return telefono
    
    def clean_capacidad_maxima(self):
        capacidad_maxima = self.cleaned_data['capacidad_maxima']
        capacidad_actual = self.cleaned_data.get('capacidad_actual', 0)
        
        if capacidad_maxima < capacidad_actual:
            raise ValidationError('La capacidad máxima no puede ser menor que la capacidad actual.')
        
        return capacidad_maxima
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            # Crear perfil de albergue
            albergue = Albergue.objects.create(
                usuario=user,
                nombre=self.cleaned_data['nombre_albergue'],
                telefono=self.cleaned_data['telefono_albergue'],
                entidad_federativa=self.cleaned_data['entidad_federativa'],
                municipio_alcaldia=self.cleaned_data['municipio_alcaldia'],
                codigo_postal=self.cleaned_data['codigo_postal'],
                calle=self.cleaned_data['calle'],
                numero_exterior=self.cleaned_data['numero_exterior'],
                referencias=self.cleaned_data['referencias'],
                nombre_responsable=self.cleaned_data['nombre_responsable'],
                apellido_responsable=self.cleaned_data['apellido_responsable'],
                correo_responsable=self.cleaned_data['correo_responsable'],
                capacidad_actual=self.cleaned_data['capacidad_actual'],
                capacidad_maxima=self.cleaned_data['capacidad_maxima'],
                facebook=self.cleaned_data['facebook'],
                instagram=self.cleaned_data['instagram'],
                twitter=self.cleaned_data['twitter'],
                sitio_web=self.cleaned_data['sitio_web'],
                imagen1=self.cleaned_data['imagen1'],
                imagen2=self.cleaned_data['imagen2'],
                imagen3=self.cleaned_data['imagen3'],
                imagen4=self.cleaned_data['imagen4']
            )
            
            # Agregar servicios seleccionados
            albergue.servicios.set(self.cleaned_data['servicios'])
        
        return user