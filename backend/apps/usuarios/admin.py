from django.contrib import admin
from .models import PerfilUsuario, LogAccion


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
