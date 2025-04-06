from patitas_a_casa.apps.perros.Avistamiento_Perros import views
from .apps.perros.Avistamiento_Perros.views import HomeView
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('avistamiento/anonimo/', views.AvistamientoAnonimoCreateView.as_view(), name='crear_avistamiento_anonimo'),
    path('avistamiento/persona/', views.AvistamientoPersonaCreateView.as_view(), name='crear_avistamiento_persona'),
    path('avistamiento/albergue/', views.AvistamientoAlbergueCreateView.as_view(), name='crear_avistamiento_albergue'),
    path('avistamiento/avistamiento-exito/', views.avistamiento_exito, name='avistamiento_exito'),
    path('avistamiento/lista/', views.ListaAvistamientosView.as_view(), name='lista_avistamientos'),
    path('avistamiento/detalle/<int:pk>/', views.DetalleAvistamientoView.as_view(), name='detalle_avistamiento'),
    path('avistamiento/', views.avistamiento_router, name='avistamiento_router'),
    path('admin/', admin.site.urls),
    path('avistamiento/exito/', views.avistamiento_exito, name='avistamiento_exito'),
    path('usuarios/', include('patitas_a_casa.apps.usuarios.urls')),
    path('avistamiento/', include('patitas_a_casa.apps.perros.Avistamiento_Perros.urls', namespace='avistamiento_perros')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)