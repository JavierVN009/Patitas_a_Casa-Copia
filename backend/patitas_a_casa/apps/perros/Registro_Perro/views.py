from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.db import transaction
from django.http import HttpResponseForbidden

from .models import PerroPerdido, FotoPerroPerdido
from .forms import PerroPerdidoForm, FotoPerroPerdidoFormSet
from apps.usuarios.models import Usuario

@method_decorator(login_required, name='dispatch')
class PerroPerdidoCreateView(CreateView):
    model = PerroPerdido
    form_class = PerroPerdidoForm
    template_name = 'registro_perro/crear_registro.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['foto_formset'] = FotoPerroPerdidoFormSet(self.request.POST, self.request.FILES)
        else:
            context['foto_formset'] = FotoPerroPerdidoFormSet()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        foto_formset = context['foto_formset']
        
        # Verificar que el usuario tenga un perfil de persona física
        try:
            propietario = Usuario.objects.get(usuario=self.request.user)
        except Usuario.DoesNotExist:
            messages.error(self.request, "Debes completar tu perfil de usuario para registrar un perro perdido.")
            return redirect('completar_perfil')
        
        with transaction.atomic():
            # Guardar el formulario principal
            self.object = form.save(commit=False)
            self.object.propietario = propietario
            self.object.save()
            
            # Guardar las fotos si el formset es válido
            if foto_formset.is_valid():
                foto_formset.instance = self.object
                foto_formset.save()
            else:
                # Si hay errores en el formset, mostrarlos y volver al formulario
                for error in foto_formset.errors:
                    messages.error(self.request, error)
                return self.form_invalid(form)
        
        messages.success(self.request, f"¡Hemos registrado a {self.object.nombre}! Esperamos que pronto puedas reencontrarte con tu mascota.")
        return redirect('registro_perro:detalle_perro', pk=self.object.pk)


@method_decorator(login_required, name='dispatch')
class PerroPerdidoUpdateView(UpdateView):
    model = PerroPerdido
    form_class = PerroPerdidoForm
    template_name = 'registro_perro/editar_registro.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['foto_formset'] = FotoPerroPerdidoFormSet(
                self.request.POST, 
                self.request.FILES, 
                instance=self.object
            )
        else:
            context['foto_formset'] = FotoPerroPerdidoFormSet(instance=self.object)
        return context
    
    def dispatch(self, request, *args, **kwargs):
        # Verificar que el usuario sea el propietario
        obj = self.get_object()
        if obj.propietario.usuario != request.user:
            messages.error(request, "No tienes permiso para editar este registro.")
            return redirect('registro_perro:mis_perros')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        context = self.get_context_data()
        foto_formset = context['foto_formset']
        
        with transaction.atomic():
            self.object = form.save()
            
            if foto_formset.is_valid():
                foto_formset.instance = self.object
                foto_formset.save()
            else:
                for error in foto_formset.errors:
                    messages.error(self.request, error)
                return self.form_invalid(form)
        
        messages.success(self.request, f"La información de {self.object.nombre} ha sido actualizada correctamente.")
        return redirect('registro_perro:detalle_perro', pk=self.object.pk)


@method_decorator(login_required, name='dispatch')
class MisPerrosPerdidosListView(ListView):
    model = PerroPerdido
    template_name = 'registro_perro/mis_perros.html'
    context_object_name = 'perros'
    
    def get_queryset(self):
        try:
            propietario = Usuario.objects.get(usuario=self.request.user)
            return PerroPerdido.objects.filter(propietario=propietario).order_by('-fecha_registro')
        except Usuario.DoesNotExist:
            return PerroPerdido.objects.none()


class PerroPerdidoDetailView(DetailView):
    model = PerroPerdido
    template_name = 'registro_perro/detalle_perro.html'
    context_object_name = 'perro'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadir fotos
        context['fotos'] = self.object.fotos.all()
        # Verificar si el usuario actual es el propietario
        if self.request.user.is_authenticated:
            try:
                usuario = Usuario.objects.get(usuario=self.request.user)
                context['es_propietario'] = (self.object.propietario == usuario)
            except Usuario.DoesNotExist:
                context['es_propietario'] = False
        else:
            context['es_propietario'] = False
        return context


@method_decorator(login_required, name='dispatch')
class PerroPerdidoDeleteView(DeleteView):
    model = PerroPerdido
    template_name = 'registro_perro/eliminar_registro.html'
    context_object_name = 'perro'
    success_url = reverse_lazy('registro_perro:mis_perros')
    
    def dispatch(self, request, *args, **kwargs):
        # Verificar que el usuario sea el propietario
        obj = self.get_object()
        if obj.propietario.usuario != request.user:
            messages.error(request, "No tienes permiso para eliminar este registro.")
            return redirect('registro_perro:mis_perros')
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        perro = self.get_object()
        nombre = perro.nombre
        messages.success(request, f"El registro de {nombre} ha sido eliminado correctamente.")
        return super().delete(request, *args, **kwargs)


@login_required
def marcar_como_encontrado(request, pk):
    perro = get_object_or_404(PerroPerdido, pk=pk)
    
    # Verificar si el usuario es el propietario
    try:
        usuario = Usuario.objects.get(usuario=request.user)
        if perro.propietario != usuario:
            messages.error(request, "No tienes permiso para realizar esta acción.")
            return redirect('registro_perro:detalle_perro', pk=perro.pk)
    except Usuario.DoesNotExist:
        messages.error(request, "No tienes un perfil de usuario válido.")
        return redirect('registro_perro:detalle_perro', pk=perro.pk)
    
    # Cambiar el estado a 'encontrado'
    perro.estado = 'encontrado'
    perro.save()
    
    messages.success(request, f"¡Qué alegría! Has marcado a {perro.nombre} como encontrado. Nos alegramos mucho por ti y por él.")
    return redirect('registro_perro:detalle_perro', pk=perro.pk)


class PerrosPerdidosListView(ListView):
    model = PerroPerdido
    template_name = 'registro_perro/lista_perros_perdidos.html'
    context_object_name = 'perros'
    paginate_by = 12
    
    def get_queryset(self):
        # Mostrar solo los perros activos (no encontrados)
        queryset = PerroPerdido.objects.filter(estado='activo').order_by('-fecha_registro')
        
        # Aplicar filtros si los hay
        entidad = self.request.GET.get('entidad')
        municipio = self.request.GET.get('municipio')
        raza = self.request.GET.get('raza')
        tamaño = self.request.GET.get('tamaño')
        
        if entidad:
            queryset = queryset.filter(entidad_federativa__icontains=entidad)
        if municipio:
            queryset = queryset.filter(municipio_alcaldia__icontains=municipio)
        if raza:
            queryset = queryset.filter(raza__icontains=raza)
        if tamaño:
            queryset = queryset.filter(tamaño=tamaño)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadir opciones para filtros
        context['entidades'] = PerroPerdido.objects.values_list('entidad_federativa', flat=True).distinct()
        context['tamaños'] = dict(PerroPerdido.TAMAÑO_CHOICES)
        # Pasar los parámetros actuales para mantener los filtros
        context['current_filters'] = self.request.GET.dict()
        return context