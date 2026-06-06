from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.views.generic import CreateView, ListView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User

from .models import PerfilUsuario, LogAccion
from .forms import RegistroPostulanteForm, CrearUsuarioStaffForm, EditarUsuarioForm
from .decoradores import AdministradorRequeridoMixin, LoginRequeridoMixin


# ──────────────────────────────────────────────
# Autenticación
# ──────────────────────────────────────────────

class LoginPersonalizadoView(LoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if hasattr(user, 'perfil'):
            if user.perfil.es_administrador() or user.perfil.es_evaluador():
                return reverse_lazy('evaluaciones:lista')
            return reverse_lazy('postulantes:panel')
        return reverse_lazy('postulantes:panel')

    def form_valid(self, form):
        response = super().form_valid(form)
        LogAccion.objects.create(
            usuario=self.request.user,
            accion='login',
            ip_address=self._get_ip(),
        )
        return response

    def _get_ip(self):
        x_forward = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forward:
            return x_forward.split(',')[0]
        return self.request.META.get('REMOTE_ADDR')


class LogoutPersonalizadoView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            LogAccion.objects.create(usuario=request.user, accion='logout')
        return super().dispatch(request, *args, **kwargs)


# ──────────────────────────────────────────────
# Registro de postulante
# ──────────────────────────────────────────────

class RegistroPostulanteView(CreateView):
    form_class = RegistroPostulanteForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('postulantes:panel')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, '¡Registro exitoso! Bienvenido al sistema de becas.')
        LogAccion.objects.create(usuario=user, accion='registro')
        return redirect(self.success_url)


# ──────────────────────────────────────────────
# Gestión de usuarios (solo administrador)
# ──────────────────────────────────────────────

class GestionUsuariosView(AdministradorRequeridoMixin, ListView):
    template_name = 'usuarios/gestion.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        return User.objects.select_related('perfil').exclude(
            pk=self.request.user.pk
        ).order_by('first_name')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_crear'] = CrearUsuarioStaffForm()
        return ctx


class CrearUsuarioStaffView(AdministradorRequeridoMixin, CreateView):
    form_class = CrearUsuarioStaffForm
    template_name = 'usuarios/crear_usuario.html'
    success_url = reverse_lazy('usuarios:gestion')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, f'Usuario {user.get_full_name()} creado correctamente.')
        LogAccion.objects.create(
            usuario=self.request.user,
            accion='crear_usuario',
            detalles={'nuevo_usuario': user.username},
        )
        return redirect(self.success_url)


class EditarUsuarioView(AdministradorRequeridoMixin, UpdateView):
    model = User
    form_class = EditarUsuarioForm
    template_name = 'usuarios/editar_usuario.html'
    success_url = reverse_lazy('usuarios:gestion')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Actualizar rol
        rol = self.request.POST.get('rol')
        if rol and hasattr(self.object, 'perfil'):
            self.object.perfil.rol = rol
            self.object.perfil.save()
        messages.success(self.request, 'Usuario actualizado correctamente.')
        LogAccion.objects.create(
            usuario=self.request.user,
            accion='modificar_usuario',
            objeto_id=self.object.pk,
        )
        return response


class ToggleUsuarioView(AdministradorRequeridoMixin, TemplateView):
    """Activar / desactivar un usuario."""
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.is_active = not user.is_active
        user.save()
        estado = 'activado' if user.is_active else 'desactivado'
        messages.success(request, f'Usuario {estado} correctamente.')
        return redirect('usuarios:gestion')


# ──────────────────────────────────────────────
# Logs de auditoría
# ──────────────────────────────────────────────

class LogsView(AdministradorRequeridoMixin, ListView):
    model = LogAccion
    template_name = 'usuarios/logs.html'
    context_object_name = 'logs'
    paginate_by = 50

    def get_queryset(self):
        qs = LogAccion.objects.select_related('usuario').order_by('-timestamp')
        accion = self.request.GET.get('accion')
        if accion:
            qs = qs.filter(accion=accion)
        usuario_id = self.request.GET.get('usuario')
        if usuario_id:
            qs = qs.filter(usuario_id=usuario_id)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['acciones'] = LogAccion.ACCION_CHOICES
        ctx['usuarios_staff'] = User.objects.filter(is_staff=True)
        return ctx
