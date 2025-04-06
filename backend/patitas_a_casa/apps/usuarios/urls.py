from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Rutas para registro
    path('registro/', views.InicioRegistroView.as_view(), name='inicio_registro'),
    path('registro/persona/', views.RegistroPersonaView.as_view(), name='registro_persona'),
    path('registro/albergue/', views.RegistroAlbergueView.as_view(), name='registro_albergue'),
    path('registro/exitoso/', views.registro_exitoso, name='registro_exitoso'),
    
    # Rutas para perfiles post-registro
    path('tipo-usuario/', views.registro_tipo_usuario, name='registro_tipo_usuario'),
    path('crear-perfil/persona/', views.crear_perfil_persona, name='crear_perfil_persona'),
    path('crear-perfil/albergue/', views.crear_perfil_albergue, name='crear_perfil_albergue'),
    
    # Rutas para ver y editar perfiles
    path('perfil/', views.ver_perfil, name='ver_perfil'),
    path('perfil/editar/persona/', views.editar_perfil_persona, name='editar_perfil_persona'),
    path('perfil/editar/albergue/', views.editar_perfil_albergue, name='editar_perfil_albergue'),
    
    # Rutas públicas para albergues
    path('albergues/', views.ListaAlberguesView.as_view(), name='lista_albergues'),
    path('albergue/<int:pk>/', views.ver_albergue, name='ver_albergue'),
]