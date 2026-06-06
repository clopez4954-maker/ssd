from django.views.generic import TemplateView, UpdateView, CreateView
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy

from .models import Postulante, DatosAcademicos, DatosSocioeconomicos
from .forms import DatosPersonalesForm, DatosAcademicosForm, DatosSocioeconomicosForm
from apps.usuarios.decoradores import PostulanteRequeridoMixin, LoginRequeridoMixin
from apps.convocatorias.models import Convocatoria
from apps.evaluaciones.models import Evaluacion


# ──────────────────────────────────────────────
# Panel del postulante
# ──────────────────────────────────────────────

class PanelPostulanteView(LoginRequeridoMixin, TemplateView):
    template_name = 'postulantes/panel.html'

    def dispatch(self, request, *args, **kwargs):
        # Redirigir evaluadores/admins a su panel
        if request.user.is_authenticated and hasattr(request.user, 'perfil'):
            if request.user.perfil.es_evaluador():
                return redirect('evaluaciones:lista')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        postulante = getattr(user, 'postulante', None)
        ctx['postulante'] = postulante
        ctx['convocatoria_activa'] = Convocatoria.objects.filter(activa=True).first()

        if postulante:
            ctx['tiene_datos_personales'] = True
            ctx['tiene_datos_academicos'] = hasattr(postulante, 'datos_academicos')
            ctx['tiene_datos_socio'] = hasattr(postulante, 'datos_socioeconomicos')
            evaluacion = getattr(postulante, 'evaluacion', None)
            ctx['evaluacion'] = evaluacion
            # % de progreso del formulario
            pasos = [True, ctx['tiene_datos_academicos'], ctx['tiene_datos_socio']]
            ctx['progreso'] = int(sum(pasos) / 3 * 100)
        else:
            ctx['tiene_datos_personales'] = False
            ctx['tiene_datos_academicos'] = False
            ctx['tiene_datos_socio'] = False
            ctx['progreso'] = 0

        return ctx


# ──────────────────────────────────────────────
# Datos personales
# ──────────────────────────────────────────────

class DatosPersonalesView(PostulanteRequeridoMixin, TemplateView):
    template_name = 'postulantes/datos_personales.html'

    def _get_convocatoria(self):
        return Convocatoria.objects.filter(activa=True).first()

    def get(self, request, *args, **kwargs):
        postulante = getattr(request.user, 'postulante', None)
        form = DatosPersonalesForm(instance=postulante)
        convocatoria = self._get_convocatoria()
        puede_editar = postulante.puede_editar if postulante else bool(convocatoria and convocatoria.esta_abierta)
        return self.render_to_response({
            'form': form, 'puede_editar': puede_editar,
            'postulante': postulante, 'convocatoria': convocatoria,
        })

    def post(self, request, *args, **kwargs):
        postulante = getattr(request.user, 'postulante', None)
        convocatoria = self._get_convocatoria()

        if postulante and not postulante.puede_editar:
            messages.error(request, 'No puedes modificar tus datos en este momento.')
            return redirect('postulantes:panel')

        form = DatosPersonalesForm(request.POST, instance=postulante)
        if form.is_valid():
            p = form.save(commit=False)
            p.user = request.user
            if convocatoria:
                p.convocatoria = convocatoria
            p.save()
            messages.success(request, 'Datos personales guardados correctamente.')
            return redirect('postulantes:datos_academicos')

        return self.render_to_response({
            'form': form, 'puede_editar': True,
            'postulante': postulante, 'convocatoria': convocatoria,
        })


# ──────────────────────────────────────────────
# Datos académicos
# ──────────────────────────────────────────────

class DatosAcademicosView(PostulanteRequeridoMixin, TemplateView):
    template_name = 'postulantes/datos_academicos.html'

    def _get_postulante(self):
        return get_object_or_404(Postulante, user=self.request.user)

    def get(self, request, *args, **kwargs):
        postulante = self._get_postulante()
        academicos = getattr(postulante, 'datos_academicos', None)
        form = DatosAcademicosForm(instance=academicos)
        return self.render_to_response({
            'form': form, 'postulante': postulante,
            'puede_editar': postulante.puede_editar,
        })

    def post(self, request, *args, **kwargs):
        postulante = self._get_postulante()
        if not postulante.puede_editar:
            messages.error(request, 'No puedes modificar tus datos en este momento.')
            return redirect('postulantes:panel')

        academicos = getattr(postulante, 'datos_academicos', None)
        form = DatosAcademicosForm(request.POST, instance=academicos)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.postulante = postulante
            obj.save()
            messages.success(request, 'Datos académicos guardados correctamente.')
            return redirect('postulantes:datos_socioeconomicos')

        return self.render_to_response({
            'form': form, 'postulante': postulante, 'puede_editar': True,
        })


# ──────────────────────────────────────────────
# Datos socioeconómicos
# ──────────────────────────────────────────────

class DatosSocioeconomicosView(PostulanteRequeridoMixin, TemplateView):
    template_name = 'postulantes/datos_socioeconomicos.html'

    def _get_postulante(self):
        return get_object_or_404(Postulante, user=self.request.user)

    def get(self, request, *args, **kwargs):
        postulante = self._get_postulante()
        socio = getattr(postulante, 'datos_socioeconomicos', None)
        form = DatosSocioeconomicosForm(instance=socio)
        return self.render_to_response({
            'form': form, 'postulante': postulante,
            'puede_editar': postulante.puede_editar,
        })

    def post(self, request, *args, **kwargs):
        postulante = self._get_postulante()
        if not postulante.puede_editar:
            messages.error(request, 'No puedes modificar tus datos en este momento.')
            return redirect('postulantes:panel')

        socio = getattr(postulante, 'datos_socioeconomicos', None)
        form = DatosSocioeconomicosForm(request.POST, instance=socio)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.postulante = postulante
            obj.save()
            messages.success(request, '¡Formulario completo! Tu solicitud ha sido registrada.')
            return redirect('postulantes:panel')

        return self.render_to_response({
            'form': form, 'postulante': postulante, 'puede_editar': True,
        })
