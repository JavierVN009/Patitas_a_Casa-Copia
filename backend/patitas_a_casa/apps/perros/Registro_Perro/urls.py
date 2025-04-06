from django.urls import path
from . import views
app_name = 'registro_perro'
urlpatterns = [

    path('crear/', views.PerroPerdidoCreateView.as_view(), name='crear_registro'),
    path('editar/<int:pk>/', views.PerroPerdidoUpdateView.as_view(), name='editar_registro'),
    path('eliminar/<int:pk>/', views.PerroPerdidoDeleteView.as_view(), name='eliminar_registro'),
    path('mis-perros/', views.MisPerrosPerdidosListView.as_view(), name='mis_perros'),
    path('detalle/<int:pk>/', views.PerroPerdidoDetailView.as_view(), name='detalle_perro'),
    path('encontrado/<int:pk>/', views.marcar_como_encontrado, name='marcar_encontrado'),
    path('buscar/', views.PerrosPerdidosListView.as_view(), name='buscar_perros'),
]