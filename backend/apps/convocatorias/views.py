from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

from apps.usuarios.decoradores import AdministradorRequeridoMixin
from apps.usuarios.models import LogAccion
from .models import Convocatoria
from .forms import ConvocatoriaForm


class ListaConvocatoriasView(AdministradorRequeridoMixin, ListView):
    model = Convocatoria
    template_name = 'convocatorias/lista.html'
    context_object_name = 'convocatorias'
    ordering = ['-fecha_inicio']


class CrearConvocatoriaView(AdministradorRequeridoMixin, CreateView):
    model = Convocatoria
    form_class = ConvocatoriaForm
    template_name = 'convocatorias/form.html'
    success_url = reverse_lazy('convocatorias:lista')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creada_por = self.request.user
        obj.save()
        messages.success(self.request, f'Convocatoria "{obj.nombre}" creada.')
        LogAccion.objects.create(
            usuario=self.request.user, accion='crear_convocatoria',
            objeto_id=obj.pk, detalles={'nombre': obj.nombre},
        )
        return redirect(self.success_url)


class EditarConvocatoriaView(AdministradorRequeridoMixin, UpdateView):
    model = Convocatoria
    form_class = ConvocatoriaForm
    template_name = 'convocatorias/form.html'
    success_url = reverse_lazy('convocatorias:lista')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Convocatoria actualizada correctamente.')
        LogAccion.objects.create(
            usuario=self.request.user, accion='modificar_convocatoria',
            objeto_id=self.object.pk,
        )
        return response
