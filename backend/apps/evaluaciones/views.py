from django.views.generic import ListView, DetailView, TemplateView, UpdateView
from django.views import View
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.db import models
from django.db.models import Q

import openpyxl

from apps.postulantes.models import Postulante, SolicitudBeca
from apps.postulantes.forms import EditarPostulanteStaffForm
from apps.parametros.forms import ObservacionEvaluacionForm
from apps.parametros.models import ParametroBeca, ReglaDesempate
from apps.usuarios.decoradores import EvaluadorRequeridoMixin, AdministradorRequeridoMixin
from apps.usuarios.models import LogAccion
from .models import Evaluacion
from .services import EvaluacionService


# ──────────────────────────────────────────────
# Panel del Evaluador
# ──────────────────────────────────────────────

class PanelEvaluadorView(EvaluadorRequeridoMixin, ListView):
    template_name = 'evaluaciones/panel_evaluador.html'
    context_object_name = 'solicitudes'

    def get_queryset(self):
        # 1. Construir orden dinámico para desempate
        order_fields = ['-puntaje_total']
        rules = ReglaDesempate.objects.filter(activo=True).order_by('orden_ejecucion')
        for rule in rules:
            prefix = '-' if rule.direccion == 'desc' else ''
            order_fields.append(prefix + rule.campo_modelo)

        # 2. Obtener solicitudes con ficha completa ordenadas, excluyendo rechazados
        qs = SolicitudBeca.objects.select_related(
            'postulante__user',
            'postulante__ficha_socioeconomica',
            'postulante__datos_academicos'
        ).filter(postulante__ficha_completada=True, rechazado=False).order_by(*order_fields)

        # Convertir a lista para asignar la posición 1-N
        solicitudes = list(qs)
        for idx, sol in enumerate(solicitudes, 1):
            sol.posicion = idx
        return solicitudes

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        param_cupos = ParametroBeca.objects.filter(nombre='cupos_disponibles').first()
        ctx['cupos_disponibles'] = int(param_cupos.valor) if param_cupos else 10
        ctx['total_completados'] = len(self.object_list)
        ctx['total_seleccionados'] = sum(1 for sol in self.object_list if sol.estado == 'Beca Asignada')
        return ctx


class EjecutarOptimizacionView(EvaluadorRequeridoMixin, View):
    def post(self, request):
        # 1. Obtener cupos disponibles
        param_cupos = ParametroBeca.objects.filter(nombre='cupos_disponibles').first()
        n_cupos = int(param_cupos.valor) if param_cupos else 10

        # 2. Construir orden dinámico para desempate
        order_fields = ['-puntaje_total']
        
        rules = ReglaDesempate.objects.filter(activo=True).order_by('orden_ejecucion')
        for rule in rules:
            prefix = '-' if rule.direccion == 'desc' else ''
            order_fields.append(prefix + rule.campo_modelo)

        # 3. Obtener solicitudes con ficha completa ordenadas, excluyendo rechazados
        solicitudes = SolicitudBeca.objects.filter(
            postulante__ficha_completada=True,
            rechazado=False
        ).order_by(*order_fields)

        total_solicitudes = solicitudes.count()

        # 4. Asignar becas
        now = timezone.now()
        seleccionados_ids = []
        
        # Tomar los primeros N
        for idx, sol in enumerate(solicitudes):
            if idx < n_cupos:
                sol.estado = 'Beca Asignada'
                sol.fecha_asignacion = now
                seleccionados_ids.append(sol.pk)
            else:
                sol.estado = 'No seleccionado'
                sol.fecha_asignacion = None
            sol.save()

        LogAccion.objects.create(
            usuario=request.user,
            accion='evaluacion',
            detalles={
                'mensaje': 'Optimización de becas ejecutada',
                'cupos': n_cupos,
                'total_postulantes': total_solicitudes,
                'seleccionados_count': len(seleccionados_ids),
            }
        )

        messages.success(
            request,
            f'Optimización ejecutada con éxito. Se asignaron {len(seleccionados_ids)} becas de {total_solicitudes} postulantes activos.'
        )
        return redirect('panel_evaluador')


class ExportarExcelView(EvaluadorRequeridoMixin, View):
    def get(self, request):
        # Crear libro Excel
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Postulantes Seleccionados"

        # Cabeceras
        headers = [
            "Nombres", "Apellidos", "Cédula", "Correo", 
            "Facultad", "Carrera", "Puntaje Académico", 
            "Puntaje Socioeconómico", "Puntaje Total (Z)", "Estado"
        ]
        ws.append(headers)

        # Obtener todas las solicitudes
        solicitudes = SolicitudBeca.objects.select_related(
            'postulante__user'
        ).filter(postulante__ficha_completada=True).order_by('-puntaje_total')

        for sol in solicitudes:
            post = sol.postulante
            user = post.user
            
            # Obtener datos de facultad y carrera
            facultad = post.facultad
            carrera = post.carrera

            ws.append([
                user.first_name,
                user.last_name,
                post.cedula,
                user.email,
                facultad,
                carrera,
                sol.puntaje_academico,
                sol.puntaje_socioeconomico,
                sol.puntaje_total,
                sol.estado
            ])

        # Formatear HttpResponse
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="reporte_seleccionados_beca.xlsx"'
        wb.save(response)
        return response


class RankingPostulantesView(EvaluadorRequeridoMixin, ListView):
    template_name = 'evaluaciones/ranking.html'
    context_object_name = 'solicitudes'

    def get_queryset(self):
        # 1. Construir orden dinámico para desempate
        order_fields = ['-puntaje_total']
        
        rules = ReglaDesempate.objects.filter(activo=True).order_by('orden_ejecucion')
        for rule in rules:
            prefix = '-' if rule.direccion == 'desc' else ''
            order_fields.append(prefix + rule.campo_modelo)

        # 2. Obtener solicitudes con ficha completa ordenadas
        qs = SolicitudBeca.objects.select_related(
            'postulante__user',
            'postulante__ficha_socioeconomica',
            'postulante__datos_academicos'
        ).filter(postulante__ficha_completada=True, rechazado=False).order_by(*order_fields)

        # Convertir a lista para asignar la posición 1-N
        solicitudes = list(qs)
        for idx, sol in enumerate(solicitudes, 1):
            sol.posicion = idx
        return solicitudes

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        param_cupos = ParametroBeca.objects.filter(nombre='cupos_disponibles').first()
        ctx['cupos_disponibles'] = int(param_cupos.valor) if param_cupos else 10
        ctx['total_completados'] = len(self.object_list)
        ctx['total_seleccionados'] = sum(1 for sol in self.object_list if sol.estado == 'Beca Asignada')
        return ctx


class ExportarRankingExcelView(EvaluadorRequeridoMixin, View):
    def get(self, request):
        order_fields = ['-puntaje_total']
        rules = ReglaDesempate.objects.filter(activo=True).order_by('orden_ejecucion')
        for rule in rules:
            prefix = '-' if rule.direccion == 'desc' else ''
            order_fields.append(prefix + rule.campo_modelo)

        solicitudes = SolicitudBeca.objects.select_related(
            'postulante__user',
            'postulante__ficha_socioeconomica',
            'postulante__datos_academicos'
        ).filter(postulante__ficha_completada=True, rechazado=False).order_by(*order_fields)

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Ranking de Postulantes"

        headers = [
            "Posición", "Nombres", "Apellidos", "Cédula", "Correo", 
            "Facultad", "Carrera", "Puntaje Académico", 
            "Puntaje Socioeconómico", "Puntaje Total (Z)", "Estado"
        ]
        ws.append(headers)

        for idx, sol in enumerate(solicitudes, 1):
            post = sol.postulante
            user = post.user
            
            facultad = post.facultad
            carrera = post.carrera

            ws.append([
                idx,
                user.first_name,
                user.last_name,
                post.cedula,
                user.email,
                facultad,
                carrera,
                sol.puntaje_academico or 0.0,
                sol.puntaje_socioeconomico or 0.0,
                sol.puntaje_total or 0.0,
                sol.estado
            ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="ranking_postulantes.xlsx"'
        wb.save(response)
        return response


# ──────────────────────────────────────────────
# Vistas Anteriores (Mantener para compatibilidad)
# ──────────────────────────────────────────────

class ListaPostulantesView(EvaluadorRequeridoMixin, ListView):
    template_name = 'evaluaciones/lista.html'
    context_object_name = 'postulantes'
    paginate_by = 20

    def get_queryset(self):
        qs = Postulante.objects.select_related(
            'ficha_socioeconomica', 'evaluacion', 'convocatoria', 'solicitud_beca'
        ).order_by('-fecha_registro')

        estado = self.request.GET.get('estado')
        if estado:
            if estado == 'Pendiente':
                qs = qs.filter(Q(solicitud_beca__isnull=True) | Q(solicitud_beca__estado='Pendiente'))
            else:
                qs = qs.filter(solicitud_beca__estado=estado)

        busqueda = self.request.GET.get('q')
        if busqueda:
            qs = qs.filter(
                cedula__icontains=busqueda
            ) | qs.filter(nombre_completo__icontains=busqueda)

        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['estados'] = [
            ('Pendiente', 'Pendiente'),
            ('Aprobado', 'Aprobado'),
            ('Rechazado', 'Rechazado'),
            ('Beca Asignada', 'Beca Asignada'),
            ('No seleccionado', 'No seleccionado'),
        ]
        ctx['filtro_estado'] = self.request.GET.get('estado', '')
        ctx['filtro_q'] = self.request.GET.get('q', '')
        ctx['total'] = self.get_queryset().count()
        return ctx


class DetallePostulanteView(EvaluadorRequeridoMixin, DetailView):
    model = Postulante
    template_name = 'evaluaciones/detalle.html'
    context_object_name = 'postulante'

    def get_queryset(self):
        return Postulante.objects.select_related(
            'ficha_socioeconomica',
            'evaluacion',
            'convocatoria',
            'user',
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['obs_form'] = ObservacionEvaluacionForm()
        ctx['evaluacion'] = getattr(self.object, 'evaluacion', None)
        ctx['solicitud_beca'] = getattr(self.object, 'solicitud_beca', None)
        ctx['tiene_datos_completos'] = hasattr(self.object, 'ficha_socioeconomica')
        return ctx

    def post(self, request, *args, **kwargs):
        from django.core.mail import send_mail
        from django.conf import settings
        
        postulante = self.get_object()
        solicitud, _ = SolicitudBeca.objects.get_or_create(postulante=postulante)

        if 'aprobar' in request.POST:
            solicitud.estado = 'Aprobado'
            solicitud.fecha_revision = timezone.now()
            solicitud.observaciones_internas = request.POST.get('observaciones_internas', '')
            solicitud.motivo_rechazo = None
            solicitud.save()

            # Registrar en LogAccion
            LogAccion.objects.create(
                usuario=request.user,
                accion='evaluacion',
                detalles={'postulante': postulante.user.username, 'nuevo_estado': 'Aprobado'},
                objeto_id=postulante.pk,
                objeto_tipo='Postulante'
            )

            messages.success(request, f'Postulación de {postulante.nombre_completo} aprobada correctamente.')
            return redirect('evaluaciones:detalle', pk=postulante.pk)

        elif 'rechazar' in request.POST:
            motivo = request.POST.get('motivo_rechazo', '').strip()
            if not motivo or len(motivo) < 10:
                messages.error(request, 'El motivo del rechazo es obligatorio y debe tener al menos 10 caracteres.')
                return redirect('evaluaciones:detalle', pk=postulante.pk)

            solicitud.estado = 'Rechazado'
            solicitud.motivo_rechazo = motivo
            solicitud.fecha_revision = timezone.now()
            solicitud.observaciones_internas = request.POST.get('observaciones_internas', '')
            solicitud.save()

            # Registrar en LogAccion
            LogAccion.objects.create(
                usuario=request.user,
                accion='evaluacion',
                detalles={'postulante': postulante.user.username, 'nuevo_estado': 'Rechazado', 'motivo': motivo},
                objeto_id=postulante.pk,
                objeto_tipo='Postulante'
            )

            # Enviar correo
            asunto = "Tu postulación a la Beca Albergue ha sido rechazada"
            cuerpo = f"Hola {postulante.user.first_name or postulante.nombre_completo},\n\nTu postulación ha sido rechazada por el siguiente motivo:\n\n{motivo}\n\nPuedes ver más detalles en tu panel de usuario en:\n{request.build_absolute_uri('/dashboard/mi-postulacion/')}"
            send_mail(
                asunto,
                cuerpo,
                getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@uagrm.edu.bo'),
                [postulante.user.email],
                fail_silently=True
            )

            messages.success(request, f'Postulación de {postulante.nombre_completo} rechazada y notificación enviada.')
            return redirect('evaluaciones:detalle', pk=postulante.pk)

        return redirect('evaluaciones:detalle', pk=postulante.pk)


class EvaluarPostulanteView(EvaluadorRequeridoMixin, TemplateView):
    def post(self, request, pk):
        postulante = get_object_or_404(
            Postulante.objects.select_related('ficha_socioeconomica'),
            pk=pk,
        )
        try:
            evaluacion = EvaluacionService.evaluar(postulante, evaluado_por=request.user)
            messages.success(
                request,
                f'Evaluación completada: {postulante.nombre_completo} → ({evaluacion.puntaje_total} pts)',
            )
        except Exception as exc:
            messages.error(request, f'Error al evaluar: {exc}')

        return redirect('evaluaciones:detalle', pk=pk)


class ReevaluarMasivoView(EvaluadorRequeridoMixin, TemplateView):
    template_name = 'evaluaciones/reevaluar_masivo.html'

    def post(self, request):
        return redirect('evaluaciones:lista')


class EditarPostulanteStaffView(EvaluadorRequeridoMixin, UpdateView):
    model = Postulante
    form_class = EditarPostulanteStaffForm
    template_name = 'evaluaciones/editar_postulante.html'

    def get_success_url(self):
        return reverse_lazy('evaluaciones:detalle', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Datos del postulante actualizados correctamente.')
        return response


from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(lambda u: u.is_staff or (hasattr(u, 'perfil') and u.perfil.es_evaluador()))
def rechazar_postulante(request, pk):
    solicitud = get_object_or_404(SolicitudBeca, postulante__pk=pk)
    if request.method == 'POST':
        motivo = request.POST.get('motivo_rechazo', '').strip()
        if not motivo or len(motivo) < 10:
            messages.error(request, 'El motivo del rechazo es obligatorio y debe tener al menos 10 caracteres.')
            return redirect('evaluaciones:detalle', pk=pk)

        notificar = request.POST.get('notificar') == 'on' or request.POST.get('notificar') == 'true'
        solicitud.rechazado = True
        solicitud.motivo_rechazo = motivo
        solicitud.fecha_rechazo = timezone.now()
        solicitud.estado = 'Rechazado'
        solicitud.notificado_rechazo = notificar
        solicitud.save()
        
        if notificar:
            from django.core.mail import send_mail
            from django.conf import settings
            asunto = "Actualización de tu postulación a la Beca Albergue UAGRM"
            cuerpo = f"Tu postulación ha sido rechazada por el siguiente motivo: {motivo}.\n\nPuedes contactar al comité de becas para más información."
            send_mail(
                asunto,
                cuerpo,
                getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@uagrm.edu.bo'),
                [solicitud.postulante.user.email],
                fail_silently=True
            )

        # Registrar en LogAccion
        LogAccion.objects.create(
            usuario=request.user,
            accion='evaluacion',
            detalles={'postulante': solicitud.postulante.user.username, 'nuevo_estado': 'Rechazado', 'motivo': motivo},
            objeto_id=solicitud.postulante.pk,
            objeto_tipo='Postulante'
        )
        
        messages.success(request, f'Postulante {solicitud.postulante.user.get_full_name()} rechazado correctamente.')
        return redirect('panel_evaluador')
    
    return redirect('evaluaciones:detalle', pk=pk)


@login_required
@user_passes_test(lambda u: u.is_staff or (hasattr(u, 'perfil') and u.perfil.es_evaluador()))
def reactivar_postulante(request, pk):
    solicitud = get_object_or_404(SolicitudBeca, postulante__pk=pk)
    solicitud.rechazado = False
    solicitud.estado = 'Pendiente'
    solicitud.motivo_rechazo = None
    solicitud.fecha_rechazo = None
    solicitud.notificado_rechazo = False
    solicitud.save()

    # Registrar en LogAccion
    LogAccion.objects.create(
        usuario=request.user,
        accion='evaluacion',
        detalles={'postulante': solicitud.postulante.user.username, 'nuevo_estado': 'Pendiente', 'mensaje': 'Postulante reactivado'},
        objeto_id=solicitud.postulante.pk,
        objeto_tipo='Postulante'
    )

    messages.success(request, f'Postulante {solicitud.postulante.user.get_full_name()} reactivado correctamente.')
    return redirect('evaluaciones:detalle', pk=pk)
