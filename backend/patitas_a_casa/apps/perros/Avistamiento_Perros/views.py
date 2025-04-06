from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .models import AvistamientoPerro
from .forms import AvistamientoAnonimoForm, AvistamientoPersonaForm, AvistamientoAlbergueForm
from patitas_a_casa.apps.usuarios.models import Usuario, Albergue
from django.views.generic import TemplateView
from django.http import JsonResponse


def home(request):  
    return render(request, 'home.html')

def determinar_tipo_usuario(request):
    """Determina si el usuario es una persona física o un albergue"""
    if not request.user.is_authenticated:
        return None
    
    try:
        return Usuario.objects.get(usuario=request.user)
    except Usuario.DoesNotExist:
        try:
            return Albergue.objects.get(usuario=request.user)
        except Albergue.DoesNotExist:
            return None
class AvistamientoAnonimoCreateView(CreateView):
    model = AvistamientoPerro
    form_class = AvistamientoAnonimoForm
    template_name = 'avistamiento/crear_avistamiento_anonimo.html'
    success_url = reverse_lazy('avistamiento_exito')
    
    def form_valid(self, form):
        print("Datos del formulario:", form.cleaned_data)  # Para depuración
        response = super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        messages.success(self.request, "¡Reporte enviado con éxito!")
        return response
    
    def form_invalid(self, form):
        print("Errores del formulario:", form.errors)  # Para depuración
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})
        return super().form_invalid(form)
    
@method_decorator(login_required, name='dispatch')
class AvistamientoPersonaCreateView(CreateView):
    model = AvistamientoPerro
    form_class = AvistamientoPersonaForm
    template_name = 'avistamiento/crear_avistamiento_persona.html'
    success_url = reverse_lazy('avistamiento_exito')
    
    def form_valid(self, form):
        usuario = Usuario.objects.get(usuario=self.request.user)
        form.instance.reportado_por_usuario = usuario
        messages.success(self.request, "¡Gracias por reportar este avistamiento! Tu ayuda es invaluable para reunir a las mascotas con sus familias.")
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        # Verificar que el usuario sea una persona física
        try:
            Usuario.objects.get(usuario=request.user)
            return super().dispatch(request, *args, **kwargs)
        except Usuario.DoesNotExist:
            messages.error(request, "No tienes permiso para acceder a esta página. Esta función es solo para personas físicas.")
            return redirect('home')

@method_decorator(login_required, name='dispatch')
class AvistamientoAlbergueCreateView(CreateView):
    model = AvistamientoPerro
    form_class = AvistamientoAlbergueForm
    template_name = 'avistamiento/crear_avistamiento_albergue.html'
    success_url = reverse_lazy('avistamiento_exito')
    
    def form_valid(self, form):
        albergue = Albergue.objects.get(usuario=self.request.user)
        form.instance.reportado_por_albergue = albergue
        messages.success(self.request, "¡Gracias por reportar este avistamiento! Su colaboración es fundamental para nuestra misión.")
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        # Verificar que el usuario sea un albergue
        try:
            Albergue.objects.get(usuario=request.user)
            return super().dispatch(request, *args, **kwargs)
        except Albergue.DoesNotExist:
            messages.error(request, "No tienes permiso para acceder a esta página. Esta función es solo para albergues.")
            return redirect('home')

def avistamiento_router(request):
    """
    Redirige al usuario al formulario correspondiente según su tipo
    """
    if not request.user.is_authenticated:
        # Usuario anónimo
        return redirect('crear_avistamiento_anonimo')
    
    tipo_usuario = determinar_tipo_usuario(request)
    
    if isinstance(tipo_usuario, Usuario):
        # Es una persona física
        return redirect('crear_avistamiento_persona')
    elif isinstance(tipo_usuario, Albergue):
        # Es un albergue
        return redirect('crear_avistamiento_albergue')
    else:
        # Usuario autenticado pero sin perfil
        messages.warning(request, "No se pudo determinar tu tipo de usuario. Por favor, completa tu perfil.")
        return redirect('home')

def avistamiento_exito(request):
    """Vista de éxito después de crear un avistamiento"""
    return render(request, 'avistamiento/avistamiento_exito.html')

class ListaAvistamientosView(ListView):
    model = AvistamientoPerro
    template_name = 'avistamiento/lista_avistamientos.html'
    context_object_name = 'avistamientos'
    paginate_by = 10
    ordering = ['-fecha_reporte']

class DetalleAvistamientoView(DetailView):
    model = AvistamientoPerro
    template_name = 'avistamiento/detalle_avistamiento.html'
    context_object_name = 'avistamiento'

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Últimos 10 avistamientos reportados
        context['avistamientos_recientes'] = AvistamientoPerro.objects.all().order_by('-fecha_reporte')[:10]
        return context
    
def crear_avistamiento_anonimo(request):
    if request.method == "POST":
        form = AvistamientoAnonimoForm(request.POST, request.FILES)
        if form.is_valid():
            avistamiento = form.save()
            return JsonResponse({ 
                "success": True,
                "message": "¡Reporte enviado con éxito!"
            })
        else:
            return JsonResponse({
                "success": False,
                "errors": form.errors
            }, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)