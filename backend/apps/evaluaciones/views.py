from django.views.generic import ListView, DetailView, TemplateView, UpdateView
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import JsonResponse

from apps.postulantes.models import Postulante
from apps.postulantes.forms import EditarPostulanteStaffForm
from apps.parametros.forms import ObservacionEvaluacionForm
from apps.usuarios.decoradores import EvaluadorRequeridoMixin, AdministradorRequeridoMixin
from apps.usuarios.models import LogAccion
from .models import Evaluacion
from .services import EvaluacionService


# ──────────────────────────────────────────────
# Lista de postulantes
# ──────────────────────────────────────────────

class ListaPostulantesView(EvaluadorRequeridoMixin, ListView):
    template_name = 'evaluaciones/lista.html'
    context_object_name = 'postulantes'
    paginate_by = 20

    def get_queryset(self):
        qs = Postulante.objects.select_related(
            'datos_academicos', 'evaluacion', 'convocatoria'
        ).order_by('-fecha_registro')

        # Filtros
        estado = self.request.GET.get('estado')
        if estado:
            qs = qs.filter(evaluacion__estado=estado)

        busqueda = self.request.GET.get('q')
        if busqueda:
            qs = qs.filter(
                cedula__icontains=busqueda
            ) | qs.filter(nombre_completo__icontains=busqueda)

        puntaje_min = self.request.GET.get('puntaje_min')
        puntaje_max = self.request.GET.get('puntaje_max')
        if puntaje_min:
            qs = qs.filter(evaluacion__puntaje_total__gte=puntaje_min)
        if puntaje_max:
            qs = qs.filter(evaluacion__puntaje_total__lte=puntaje_max)

        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['estados'] = Evaluacion.ESTADO_CHOICES
        ctx['filtro_estado'] = self.request.GET.get('estado', '')
        ctx['filtro_q'] = self.request.GET.get('q', '')
        ctx['filtro_pmin'] = self.request.GET.get('puntaje_min', '')
        ctx['filtro_pmax'] = self.request.GET.get('puntaje_max', '')
        ctx['total'] = self.get_queryset().count()
        return ctx


# ──────────────────────────────────────────────
# Detalle de postulante
# ──────────────────────────────────────────────

class DetallePostulanteView(EvaluadorRequeridoMixin, DetailView):
    model = Postulante
    template_name = 'evaluaciones/detalle.html'
    context_object_name = 'postulante'

    def get_queryset(self):
        return Postulante.objects.select_related(
            'datos_academicos',
            'datos_socioeconomicos',
            'evaluacion',
            'convocatoria',
            'user',
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['obs_form'] = ObservacionEvaluacionForm()
        ctx['evaluacion'] = getattr(self.object, 'evaluacion', None)
        ctx['tiene_datos_completos'] = (
            hasattr(self.object, 'datos_academicos')
            and hasattr(self.object, 'datos_socioeconomicos')
        )
        return ctx


# ──────────────────────────────────────────────
# Evaluación automática individual
# ──────────────────────────────────────────────

class EvaluarPostulanteView(EvaluadorRequeridoMixin, TemplateView):
    def post(self, request, pk):
        postulante = get_object_or_404(
            Postulante.objects.select_related('datos_academicos', 'datos_socioeconomicos'),
            pk=pk,
        )
        try:
            evaluacion = EvaluacionService.evaluar(postulante, evaluado_por=request.user)
            LogAccion.objects.create(
                usuario=request.user,
                accion='evaluacion',
                objeto_id=postulante.pk,
                objeto_tipo='Postulante',
                detalles={
                    'puntaje_total': str(evaluacion.puntaje_total),
                    'estado': evaluacion.estado,
                },
            )
            messages.success(
                request,
                f'Evaluación completada: {postulante.nombre_completo} → '
                f'{evaluacion.get_estado_display()} ({evaluacion.puntaje_total} pts)',
            )
        except Exception as exc:
            messages.error(request, f'Error al evaluar: {exc}')

        # Soporte HTMX: devolver fragmento parcial
        if request.htmx:
            evaluacion = getattr(postulante, 'evaluacion', None)
            from django.template.loader import render_to_string
            html = render_to_string(
                'evaluaciones/_badge_estado.html',
                {'evaluacion': evaluacion},
                request=request,
            )
            return JsonResponse({'html': html})

        return redirect('evaluaciones:detalle', pk=pk)


# ──────────────────────────────────────────────
# Reevaluación masiva
# ──────────────────────────────────────────────

class ReevaluarMasivoView(EvaluadorRequeridoMixin, TemplateView):
    template_name = 'evaluaciones/reevaluar_masivo.html'

    def post(self, request):
        estado_filtro = request.POST.get('estado', '')
        qs = Postulante.objects.select_related(
            'datos_academicos', 'datos_socioeconomicos'
        )
        if estado_filtro:
            qs = qs.filter(evaluacion__estado=estado_filtro)

        evaluados, errores = EvaluacionService.reevaluar_masivo(qs, evaluado_por=request.user)

        LogAccion.objects.create(
            usuario=request.user,
            accion='reevaluacion_masiva',
            detalles={
                'evaluados': len(evaluados),
                'errores': len(errores),
                'filtro_estado': estado_filtro,
            },
        )

        messages.success(
            request,
            f'Reevaluación masiva completada: {len(evaluados)} evaluados, {len(errores)} errores.',
        )
        return redirect('evaluaciones:lista')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['estados'] = Evaluacion.ESTADO_CHOICES
        ctx['total_postulantes'] = Postulante.objects.count()
        return ctx


# ──────────────────────────────────────────────
# Editar datos del postulante (staff)
# ──────────────────────────────────────────────

class EditarPostulanteStaffView(EvaluadorRequeridoMixin, UpdateView):
    model = Postulante
    form_class = EditarPostulanteStaffForm
    template_name = 'evaluaciones/editar_postulante.html'

    def get_success_url(self):
        return reverse_lazy('evaluaciones:detalle', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        LogAccion.objects.create(
            usuario=self.request.user,
            accion='modificar_postulante',
            objeto_id=self.object.pk,
            objeto_tipo='Postulante',
            detalles={'campos': list(form.changed_data)},
        )
        messages.success(self.request, 'Datos del postulante actualizados correctamente.')
        return response
