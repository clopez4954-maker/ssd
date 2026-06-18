from django.contrib import admin
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import PerfilUsuario, LogAccion
from apps.postulantes.models import Postulante


from django.contrib.auth.models import Group


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'activo', 'fecha_creacion')
    list_filter = ('rol', 'activo')
    search_fields = ('user__username', 'user__email', 'user__first_name')
    raw_id_fields = ('user',)


@admin.register(LogAccion)
class LogAccionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'accion', 'timestamp', 'objeto_tipo', 'ip_address')
    list_filter = ('accion', 'timestamp')
    search_fields = ('usuario__username', 'accion', 'detalles')
    readonly_fields = ('usuario', 'accion', 'timestamp', 'detalles', 'ip_address')
    ordering = ('-timestamp',)
