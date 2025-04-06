from django.contrib import admin
from .models import Usuario, Albergue, ServicioAlbergue

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'telefono')

@admin.register(Albergue)
class AlbergueAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'entidad_federativa', 'municipio_alcaldia')

@admin.register(ServicioAlbergue)
class ServicioAlbergueAdmin(admin.ModelAdmin):
    list_display = ('nombre',)