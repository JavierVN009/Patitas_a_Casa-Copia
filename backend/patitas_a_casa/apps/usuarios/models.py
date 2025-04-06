from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Usuario(models.Model):
    """
    Modelo para usuarios tipo persona física.
    Relacionado con el modelo User de Django para autenticación.
    """
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario_persona')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Usuario Persona"
        verbose_name_plural = "Usuarios Personas"
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Albergue(models.Model):
    """
    Modelo para usuarios tipo albergue.
    Relacionado con el modelo User de Django para autenticación.
    """
    SERVICIOS_CHOICES = [
        ('VAC', 'Vacunación'),
        ('EST', 'Esterilización'),
        ('ADO', 'Adopción'),
        ('RES', 'Rescate'),
        ('HOG', 'Hogar Temporal'),
        ('VET', 'Atención Veterinaria'),
        ('ALI', 'Alimentación'),
        ('OTR', 'Otros'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='albergue')
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    
    # Ubicación
    entidad_federativa = models.CharField(max_length=100)
    municipio_alcaldia = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=5)
    calle = models.CharField(max_length=200)
    numero_exterior = models.CharField(max_length=20)
    referencias = models.TextField(blank=True, null=True)
    
    # Información del responsable
    nombre_responsable = models.CharField(max_length=100)
    apellido_responsable = models.CharField(max_length=100)
    correo_responsable = models.EmailField()
    
    # Información del albergue
    capacidad_actual = models.PositiveIntegerField(default=0)
    capacidad_maxima = models.PositiveIntegerField(default=0)
    servicios = models.ManyToManyField('ServicioAlbergue')
    
    # Redes sociales
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    sitio_web = models.URLField(blank=True, null=True)
    
    # Imágenes
    imagen1 = models.ImageField(upload_to='albergues/', blank=True, null=True)
    imagen2 = models.ImageField(upload_to='albergues/', blank=True, null=True)
    imagen3 = models.ImageField(upload_to='albergues/', blank=True, null=True)
    imagen4 = models.ImageField(upload_to='albergues/', blank=True, null=True)
    
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Albergue"
        verbose_name_plural = "Albergues"
    
    def __str__(self):
        return self.nombre

class ServicioAlbergue(models.Model):
    """
    Modelo para los servicios que ofrece un albergue.
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Servicio de Albergue"
        verbose_name_plural = "Servicios de Albergue"
    
    def __str__(self):
        return self.nombre

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """
    Signal para crear automáticamente un perfil vacío cuando se crea un usuario.
    No se utiliza directamente, pero puede ser útil para implementaciones futuras.
    """
    # Este código está comentado porque queremos que el usuario elija explícitamente
    # qué tipo de perfil crear (persona o albergue)
    """
    if created:
        # Puede ser implementado según la lógica de negocio
        pass
    """