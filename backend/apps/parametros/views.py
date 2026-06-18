from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy

from apps.usuarios.decoradores import AdministradorRequeridoMixin, EvaluadorRequeridoMixin
from apps.usuarios.models import LogAccion
from apps.evaluaciones.services import EvaluacionService
from apps.postulantes.models import Postulante
from .models import ParametroBeca
from .forms import ParametroBecaForm


class ListaParametrosView(EvaluadorRequeridoMixin, ListView):
    model = ParametroBeca
    template_name = 'parametros/lista.html'
    context_object_name = 'parametros'

    def get_queryset(self):
        return ParametroBeca.objects.all().order_by('nombre')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = ParametroBecaForm()
        return ctx


class CrearParametroView(AdministradorRequeridoMixin, CreateView):
    model = ParametroBeca
    form_class = ParametroBecaForm
    template_name = 'parametros/form.html'
    success_url = reverse_lazy('parametros:lista')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.modificado_por = self.request.user
        obj.save()
        messages.success(self.request, f'Parámetro "{obj.nombre}" creado.')
        LogAccion.objects.create(
            usuario=self.request.user, accion='modificar_parametro',
            detalles={'parametro': obj.nombre, 'valor': str(obj.valor), 'accion': 'crear'},
        )
        return redirect(self.success_url)


class EditarParametroView(AdministradorRequeridoMixin, UpdateView):
    model = ParametroBeca
    form_class = ParametroBecaForm
    template_name = 'parametros/form.html'

    def get_success_url(self):
        return reverse_lazy('parametros:lista')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.modificado_por = self.request.user
        obj.save()

        # Recalcular todos los puntajes automáticamente
        qs_todos = Postulante.objects.select_related(
            'ficha_socioeconomica'
        ).filter(ficha_socioeconomica__isnull=False)
        evaluados, errores = EvaluacionService.reevaluar_masivo(qs_todos, evaluado_por=self.request.user)

        messages.success(
            self.request,
            f'Parámetro actualizado. Se recalcularon {len(evaluados)} puntajes automáticamente.',
        )
        LogAccion.objects.create(
            usuario=self.request.user, accion='modificar_parametro',
            detalles={
                'parametro': obj.nombre, 'valor': str(obj.valor),
                'recalculados': len(evaluados),
            },
        )
        return redirect(self.get_success_url())
