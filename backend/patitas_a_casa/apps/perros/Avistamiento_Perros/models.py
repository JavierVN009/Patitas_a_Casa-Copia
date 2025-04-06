from django.db import models
from django.utils import timezone
from patitas_a_casa.apps.usuarios.models import Usuario, Albergue

class AvistamientoPerro(models.Model):
    SEXO_CHOICES = [
        ('M', 'Macho'),
        ('H', 'Hembra'),
        ('D', 'Desconocido'),
    ]
    
    TAMAÑO_CHOICES = [
        ('P', 'Pequeño'),
        ('M', 'Mediano'),
        ('G', 'Grande'),
        ('Gi', 'Gigante'),
    ]
    
    ESTADO_CHOICES = [
        ('S', 'Saludable'),
        ('H', 'Herido'),
        ('D', 'Desnutrido'),
        ('E', 'Enfermo'),
        ('Ag', 'Agresivo'),
        ('As', 'Asustado'),
    ]
    
    # Campos comunes para todos los tipos de avistamiento
    fecha_hora_avistamiento = models.DateTimeField(default=timezone.now)
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    
    # Ubicación
    entidad_federativa = models.CharField(max_length=100)
    municipio_alcaldia = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=5)
    colonia = models.CharField(max_length=100)
    calle = models.CharField(max_length=200)
    numero_exterior = models.CharField(max_length=20)
    
    # Información del perro
    foto = models.ImageField(upload_to='avistamientos/', blank=True, null=True)
    raza = models.CharField(max_length=100, blank=True, null=True)
    sexo = models.CharField(max_length=30, choices=SEXO_CHOICES, default='D')
    tamaño = models.CharField(max_length=10, choices=TAMAÑO_CHOICES)
    color_dominante = models.CharField(max_length=50)
    señas_particulares = models.TextField(blank=True, null=True)
    identificador = models.CharField(max_length=200, blank=True, null=True, help_text="Collar, placa, chip, etc.")
    estado_perro = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='S')
    descripcion = models.TextField()
    
    # Tipo de avistamiento y relaciones
    es_anonimo = models.BooleanField(default=False)
    reportado_por_usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    reportado_por_albergue = models.ForeignKey(Albergue, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Campo adicional para personas físicas
    puede_albergar = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Avistamiento de Perro"
        verbose_name_plural = "Avistamientos de Perros"
        ordering = ['-fecha_reporte']
    
    def __str__(self):
        ubicacion = f"{self.municipio_alcaldia}, {self.entidad_federativa}"
        if self.es_anonimo:
            return f"Avistamiento anónimo en {ubicacion} - {self.fecha_hora_avistamiento.strftime('%d/%m/%Y %H:%M')}"
        elif self.reportado_por_usuario:
            return f"Avistamiento por {self.reportado_por_usuario.nombre} en {ubicacion} - {self.fecha_hora_avistamiento.strftime('%d/%m/%Y %H:%M')}"
        else:
            return f"Avistamiento por {self.reportado_por_albergue.nombre} en {ubicacion} - {self.fecha_hora_avistamiento.strftime('%d/%m/%Y %H:%M')}"