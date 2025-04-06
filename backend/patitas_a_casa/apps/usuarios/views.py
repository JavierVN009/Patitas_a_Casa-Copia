from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, TemplateView

from .forms import (
    RegistroUsuarioForm, PerfilPersonaForm, AlbergueForm,
    RegistroCompletoPersonaForm, RegistroCompletoAlbergueForm
)
from .models import Usuario, Albergue, ServicioAlbergue

class InicioRegistroView(TemplateView):
    """Vista para elegir el tipo de registro (persona o albergue)"""
    template_name = 'usuarios/inicio_registro.html'

class RegistroPersonaView(CreateView):
    """Vista para registrar un nuevo usuario como persona física"""
    form_class = RegistroCompletoPersonaForm
    template_name = 'usuarios/registro_persona.html'
    success_url = reverse_lazy('usuarios:registro_exitoso')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Autenticar y loguear al usuario después del registro
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        messages.success(self.request, '¡Registro exitoso! Bienvenido a Patitas a Casa.')
        return response

class RegistroAlbergueView(CreateView):
    """Vista para registrar un nuevo usuario como albergue"""
    form_class = RegistroCompletoAlbergueForm
    template_name = 'usuarios/registro_albergue.html'
    success_url = reverse_lazy('usuarios:registro_exitoso')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servicios'] = ServicioAlbergue.objects.all()
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Autenticar y loguear al usuario después del registro
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        messages.success(self.request, '¡Registro exitoso! Tu albergue ha sido registrado en Patitas a Casa.')
        return response

@login_required
def registro_tipo_usuario(request):
    """Vista para elegir qué tipo de perfil crear después de registrarse"""
    # Verificar si el usuario ya tiene un perfil
    try:
        # Si ya tiene un perfil de persona
        usuario = Usuario.objects.get(usuario=request.user)
        messages.info(request, 'Ya tienes un perfil de persona registrado.')
        return redirect('home')
    except Usuario.DoesNotExist:
        try:
            # Si ya tiene un perfil de albergue
            albergue = Albergue.objects.get(usuario=request.user)
            messages.info(request, 'Ya tienes un perfil de albergue registrado.')
            return redirect('home')
        except Albergue.DoesNotExist:
            # No tiene ningún perfil, mostrar opciones
            return render(request, 'usuarios/elegir_tipo_usuario.html')

@login_required
def crear_perfil_persona(request):
    """Vista para crear un perfil de persona para un usuario ya registrado"""
    # Verificar si ya tiene algún perfil
    try:
        Usuario.objects.get(usuario=request.user)
        messages.warning(request, 'Ya tienes un perfil de persona registrado.')
        return redirect('home')
    except Usuario.DoesNotExist:
        try:
            Albergue.objects.get(usuario=request.user)
            messages.error(request, 'Ya tienes un perfil de albergue y no puedes tener ambos tipos de perfil.')
            return redirect('home')
        except Albergue.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = PerfilPersonaForm(request.POST)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.usuario = request.user
            perfil.save()
            messages.success(request, 'Perfil de persona creado exitosamente.')
            return redirect('home')
    else:
        form = PerfilPersonaForm()
    
    return render(request, 'usuarios/crear_perfil_persona.html', {'form': form})

@login_required
def crear_perfil_albergue(request):
    """Vista para crear un perfil de albergue para un usuario ya registrado"""
    # Verificar si ya tiene algún perfil
    try:
        Albergue.objects.get(usuario=request.user)
        messages.warning(request, 'Ya tienes un perfil de albergue registrado.')
        return redirect('home')
    except Albergue.DoesNotExist:
        try:
            Usuario.objects.get(usuario=request.user)
            messages.error(request, 'Ya tienes un perfil de persona y no puedes tener ambos tipos de perfil.')
            return redirect('home')
        except Usuario.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = AlbergueForm(request.POST, request.FILES)
        if form.is_valid():
            albergue = form.save(commit=False)
            albergue.usuario = request.user
            albergue.save()
            # Para el many-to-many
            form.save_m2m()
            messages.success(request, 'Perfil de albergue creado exitosamente.')
            return redirect('home')
    else:
        form = AlbergueForm()
    
    return render(request, 'usuarios/crear_perfil_albergue.html', {'form': form})

@login_required
def editar_perfil_persona(request):
    """Vista para editar un perfil de persona"""
    try:
        perfil = Usuario.objects.get(usuario=request.user)
    except Usuario.DoesNotExist:
        messages.error(request, 'No tienes un perfil de persona para editar.')
        return redirect('home')
    
    if request.method == 'POST':
        form = PerfilPersonaForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('usuarios:ver_perfil')
    else:
        form = PerfilPersonaForm(instance=perfil)
    
    return render(request, 'usuarios/editar_perfil_persona.html', {'form': form})

@login_required
def editar_perfil_albergue(request):
    """Vista para editar un perfil de albergue"""
    try:
        albergue = Albergue.objects.get(usuario=request.user)
    except Albergue.DoesNotExist:
        messages.error(request, 'No tienes un perfil de albergue para editar.')
        return redirect('home')
    
    if request.method == 'POST':
        form = AlbergueForm(request.POST, request.FILES, instance=albergue)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil de albergue actualizado exitosamente.')
            return redirect('usuarios:ver_perfil')
    else:
        form = AlbergueForm(instance=albergue)
    
    return render(request, 'usuarios/editar_perfil_albergue.html', {'form': form})

@login_required
def ver_perfil(request):
    """Vista para ver el perfil del usuario actual"""
    try:
        perfil = Usuario.objects.get(usuario=request.user)
        template = 'usuarios/perfil_persona.html'
        context = {'perfil': perfil, 'tipo': 'persona'}
    except Usuario.DoesNotExist:
        try:
            perfil = Albergue.objects.get(usuario=request.user)
            template = 'usuarios/perfil_albergue.html'
            context = {'perfil': perfil, 'tipo': 'albergue'}
        except Albergue.DoesNotExist:
            messages.warning(request, 'No tienes un perfil completo. Por favor, crea uno.')
            return redirect('usuarios:registro_tipo_usuario')
    
    return render(request, template, context)

def ver_albergue(request, pk):
    """Vista pública para ver el perfil de un albergue"""
    albergue = get_object_or_404(Albergue, pk=pk, activo=True)
    return render(request, 'usuarios/ver_albergue.html', {'albergue': albergue})

class ListaAlberguesView(ListView):
    """Vista para listar todos los albergues activos"""
    model = Albergue
    template_name = 'usuarios/lista_albergues.html'
    context_object_name = 'albergues'
    paginate_by = 10
    
    def get_queryset(self):
        return Albergue.objects.filter(activo=True).order_by('nombre')

def registro_exitoso(request):
    """Vista de éxito después del registro"""
    return render(request, 'usuarios/registro_exitoso.html')