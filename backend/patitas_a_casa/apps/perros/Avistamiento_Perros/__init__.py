from django.apps import AppConfig
default_app_config = 'apps.perros.Avistamiento_Perros.apps.AvistamientoPerrosConfig'

class AvistamientoPerrosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.perros.Avistamiento_Perros'
    verbose_name = 'Avistamientos de Perros'