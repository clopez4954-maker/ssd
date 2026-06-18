"""
Decoradores y mixins de seguridad para proteger vistas por rol.
"""
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


# ──────────────────────────────────────────────
# Helpers de rol
# ──────────────────────────────────────────────

def es_evaluador(user):
    """True si el usuario tiene rol evaluador o administrador."""
    return (
        user.is_authenticated
        and hasattr(user, 'perfil')
        and user.perfil.es_evaluador()
    )


def es_administrador(user):
    """True si el usuario tiene rol administrador."""
    return (
        user.is_authenticated
        and hasattr(user, 'perfil')
        and user.perfil.es_administrador()
    )


def es_postulante(user):
    """True si el usuario tiene rol postulante."""
    return (
        user.is_authenticated
        and hasattr(user, 'perfil')
        and user.perfil.es_postulante()
    )


# ──────────────────────────────────────────────
# Decoradores
# ──────────────────────────────────────────────

def evaluador_requerido(view_func):
    """Requiere que el usuario sea evaluador o administrador."""
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        if not es_evaluador(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped


def administrador_requerido(view_func):
    """Requiere que el usuario sea administrador."""
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        if not es_administrador(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped


# ──────────────────────────────────────────────
# Mixins para Class-Based Views
# ──────────────────────────────────────────────

class LoginRequeridoMixin:
    """Redirige al login si no está autenticado."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('usuarios:login')
        return super().dispatch(request, *args, **kwargs)


class EvaluadorRequeridoMixin(LoginRequeridoMixin):
    """Solo para evaluadores y administradores."""
    def dispatch(self, request, *args, **kwargs):
        result = super().dispatch(request, *args, **kwargs)
        if hasattr(result, 'status_code') and result.status_code == 302:
            return result
        if not es_evaluador(request.user):
            raise PermissionDenied
        return result


class AdministradorRequeridoMixin(LoginRequeridoMixin):
    """Solo para administradores."""
    def dispatch(self, request, *args, **kwargs):
        result = super().dispatch(request, *args, **kwargs)
        if hasattr(result, 'status_code') and result.status_code == 302:
            return result
        if not es_administrador(request.user):
            raise PermissionDenied
        return result


class PostulanteRequeridoMixin(LoginRequeridoMixin):
    """Solo para postulantes."""
    def dispatch(self, request, *args, **kwargs):
        result = super().dispatch(request, *args, **kwargs)
        if hasattr(result, 'status_code') and result.status_code == 302:
            return result
        if not es_postulante(request.user):
            raise PermissionDenied
        return result
