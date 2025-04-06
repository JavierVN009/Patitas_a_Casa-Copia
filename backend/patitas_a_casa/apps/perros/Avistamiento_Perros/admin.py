from django.contrib import admin
from .models import AvistamientoPerro

@admin.register(AvistamientoPerro)
class AvistamientoPerroAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_tipo_usuario', 'get_reportante', 'fecha_hora_avistamiento', 
                   'entidad_federativa', 'municipio_alcaldia', 'tamaño', 'estado_perro')
    list_filter = ('es_anonimo', 'tamaño', 'estado_perro', 'entidad_federativa')
    search_fields = ('entidad_federativa', 'municipio_alcaldia', 'colonia', 'descripcion', 'raza')
    date_hierarchy = 'fecha_reporte'
    fieldsets = (
        ('Información del Reporte', {
            'fields': ('fecha_hora_avistamiento', 'fecha_reporte', 'es_anonimo', 
                      'reportado_por_usuario', 'reportado_por_albergue')
        }),
        ('Ubicación', {
            'fields': ('entidad_federativa', 'municipio_alcaldia', 'codigo_postal', 
                      'colonia', 'calle', 'numero_exterior')
        }),
        ('Información del Perro', {
            'fields': ('foto', 'raza', 'sexo', 'tamaño', 'color_dominante', 
                      'señas_particulares', 'identificador', 'estado_perro')
        }),
        ('Información Adicional', {
            'fields': ('descripcion', 'puede_albergar')
        }),
    )
    readonly_fields = ('fecha_reporte',)
    
    def get_tipo_usuario(self, obj):
        if obj.es_anonimo:
            return "Anónimo"
        elif obj.reportado_por_usuario:
            return "Persona"
        elif obj.reportado_por_albergue:
            return "Albergue"
        return "Desconocido"
    get_tipo_usuario.short_description = "Tipo de usuario"
    
    def get_reportante(self, obj):
        if obj.es_anonimo:
            return "Anónimo"
        elif obj.reportado_por_usuario:
            return f"{obj.reportado_por_usuario.nombre} {obj.reportado_por_usuario.apellido}"
        elif obj.reportado_por_albergue:
            return obj.reportado_por_albergue.nombre
        return "Desconocido"
    get_reportante.short_description = "Reportante"
    
    def has_add_permission(self, request):
        # Solo para visualización en el admin
        return False