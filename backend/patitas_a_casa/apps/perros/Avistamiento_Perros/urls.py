from django.urls import path
from . import views
from .views import HomeView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'avistamiento_perros'

urlpatterns = [
    path('reportar/', views.avistamiento_router, name='reportar_avistamiento'),
    path('reportar/anonimo/', views.AvistamientoAnonimoCreateView.as_view(), name='crear_avistamiento_anonimo'),
    path('reportar/persona/', views.AvistamientoPersonaCreateView.as_view(), name='crear_avistamiento_persona'),
    path('reportar/albergue/', views.AvistamientoAlbergueCreateView.as_view(), name='crear_avistamiento_albergue'),
    path('exito/', views.avistamiento_exito, name='avistamiento_exito'),
    path('lista/', views.ListaAvistamientosView.as_view(), name='lista_avistamientos'),
    path('detalle/<int:pk>/', views.DetalleAvistamientoView.as_view(), name='detalle_avistamiento'),
    path('', HomeView.as_view(), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)