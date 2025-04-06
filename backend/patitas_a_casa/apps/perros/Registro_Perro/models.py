from django.db import models
from django.utils import timezone
#from apps.usuarios.models import Usuario
from patitas_a_casa.apps.usuarios.models import Usuario

class PerroPerdido(models.Model):
    SEXO_CHOICES = [
        ('M', 'Macho'),
        ('H', 'Hembra'),
    ]
    
    TAMAÑO_CHOICES = [
        ('P', 'Pequeño'),
        ('M', 'Mediano'),
        ('G', 'Grande'),
    ]
    
    COLOR_CHOICES = [
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
    
    PELAJE_CHOICES = [
        ('alambre', 'Alambre'),
        ('corto', 'Corto'),
        ('doble_capa', 'Doble capa'),
        ('duro', 'Duro'),
        ('lanoso', 'Lanoso'),
        ('largo', 'Largo'),
        ('pelaje_nuevo', 'Pelaje nuevo'),
        ('sin_pelo', 'Sin pelo'),
    ]
    
    # Información general del perro
    nombre = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    edad_años = models.PositiveIntegerField(default=0)
    edad_meses = models.PositiveIntegerField(default=0)
    tamaño = models.CharField(max_length=1, choices=TAMAÑO_CHOICES)
    raza = models.CharField(max_length=100)
    esterilizado = models.BooleanField(default=False)
    
    # Apariencia del perro
    # Uso de ManyToManyField para almacenar múltiples colores
    colores = models.CharField(max_length=500, help_text="Colores separados por coma")
    patron_pelaje = models.CharField(max_length=20, choices=PELAJE_CHOICES)
    señas_particulares = models.TextField(blank=True, null=True)
    
    # Accesorios e identificación
    tiene_collar = models.BooleanField(default=False)
    color_collar = models.CharField(max_length=50, blank=True, null=True)
    identificador = models.CharField(max_length=200, blank=True, null=True, help_text="Chip, placa, etc.")
    
    # Lugar y momento en que se perdió
    entidad_federativa = models.CharField(max_length=100)
    municipio_alcaldia = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=5)
    colonia = models.CharField(max_length=100)
    calle = models.CharField(max_length=200)
    numero_exterior = models.CharField(max_length=20)
    fecha_hora_perdida = models.DateTimeField(default=timezone.now)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    # Relación con el propietario
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='perros_perdidos')
    
    # Estado del reporte
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('encontrado', 'Encontrado'),
        ('cerrado', 'Cerrado'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Fotos del perro
    # Las fotos se manejarán con un modelo separado para permitir múltiples fotos
    
    class Meta:
        verbose_name = "Perro Perdido"
        verbose_name_plural = "Perros Perdidos"
        ordering = ['-fecha_registro']
    
    def __str__(self):
        return f"{self.nombre} - {self.raza} - {self.get_estado_display()}"
    
    def get_edad_formateada(self):
        if self.edad_años > 0 and self.edad_meses > 0:
            return f"{self.edad_años} {'año' if self.edad_años == 1 else 'años'} y {self.edad_meses} {'mes' if self.edad_meses == 1 else 'meses'}"
        elif self.edad_años > 0:
            return f"{self.edad_años} {'año' if self.edad_años == 1 else 'años'}"
        else:
            return f"{self.edad_meses} {'mes' if self.edad_meses == 1 else 'meses'}"
    
    def get_tiempo_perdido(self):
        ahora = timezone.now()
        diferencia = ahora - self.fecha_hora_perdida
        dias = diferencia.days
        
        if dias == 0:
            horas = diferencia.seconds // 3600
            if horas == 0:
                minutos = diferencia.seconds // 60
                return f"{minutos} {'minuto' if minutos == 1 else 'minutos'}"
            return f"{horas} {'hora' if horas == 1 else 'horas'}"
        elif dias < 30:
            return f"{dias} {'día' if dias == 1 else 'días'}"
        elif dias < 365:
            meses = dias // 30
            return f"{meses} {'mes' if meses == 1 else 'meses'}"
        else:
            años = dias // 365
            meses = (dias % 365) // 30
            if meses == 0:
                return f"{años} {'año' if años == 1 else 'años'}"
            return f"{años} {'año' if años == 1 else 'años'} y {meses} {'mes' if meses == 1 else 'meses'}"


class FotoPerroPerdido(models.Model):
    perro = models.ForeignKey(PerroPerdido, on_delete=models.CASCADE, related_name='fotos')
    foto = models.ImageField(upload_to='perros_perdidos/', help_text="Máximo 10MB")
    es_principal = models.BooleanField(default=False)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Foto de Perro Perdido"
        verbose_name_plural = "Fotos de Perros Perdidos"
        ordering = ['-es_principal', '-fecha_subida']
    
    def __str__(self):
        return f"Foto de {self.perro.nombre} - {'Principal' if self.es_principal else 'Secundaria'}"
    
    def save(self, *args, **kwargs):
        # Si esta foto se marca como principal, desmarcar las demás
        if self.es_principal:
            FotoPerroPerdido.objects.filter(perro=self.perro, es_principal=True).update(es_principal=False)
        
        # Si es la primera foto, marcarla como principal
        if not FotoPerroPerdido.objects.filter(perro=self.perro).exists():
            self.es_principal = True
            
        super().save(*args, **kwargs)