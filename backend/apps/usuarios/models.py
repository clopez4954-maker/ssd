from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):
    """Perfil extendido del usuario Django — asigna el rol del sistema."""

    ROL_POSTULANTE = 'postulante'
    ROL_EVALUADOR = 'evaluador'
    ROL_ADMINISTRADOR = 'administrador'

    ROL_CHOICES = [
        (ROL_POSTULANTE, 'Postulante'),
        (ROL_EVALUADOR, 'Evaluador'),
        (ROL_ADMINISTRADOR, 'Administrador'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil',
        verbose_name='Usuario',
    )
    rol = models.CharField(
        max_length=20,
        choices=ROL_CHOICES,
        default=ROL_POSTULANTE,
        verbose_name='Rol',
    )
    telefono = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username} ({self.get_rol_display()})'

    def es_postulante(self):
        return self.rol == self.ROL_POSTULANTE

    def es_evaluador(self):
        return self.rol in (self.ROL_EVALUADOR, self.ROL_ADMINISTRADOR)

    def es_administrador(self):
        return self.rol == self.ROL_ADMINISTRADOR


class LogAccion(models.Model):
    """Registro de auditoría de acciones del sistema."""

    ACCION_CHOICES = [
        ('login', 'Inicio de sesión'),
        ('logout', 'Cierre de sesión'),
        ('registro', 'Registro de postulante'),
        ('evaluacion', 'Evaluación realizada'),
        ('reevaluacion_masiva', 'Reevaluación masiva'),
        ('modificar_postulante', 'Modificación de datos de postulante'),
        ('modificar_parametro', 'Modificación de parámetro'),
        ('crear_convocatoria', 'Creación de convocatoria'),
        ('modificar_convocatoria', 'Modificación de convocatoria'),
        ('exportar', 'Exportación de datos'),
        ('crear_usuario', 'Creación de usuario'),
        ('modificar_usuario', 'Modificación de usuario'),
        ('otro', 'Otra acción'),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='logs',
        verbose_name='Usuario',
    )
    accion = models.CharField(max_length=50, choices=ACCION_CHOICES, verbose_name='Acción')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y hora')
    detalles = models.JSONField(default=dict, blank=True, verbose_name='Detalles')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='Dirección IP')
    objeto_id = models.PositiveIntegerField(null=True, blank=True, verbose_name='ID del objeto')
    objeto_tipo = models.CharField(max_length=100, blank=True, verbose_name='Tipo de objeto')

    class Meta:
        verbose_name = 'Log de Acción'
        verbose_name_plural = 'Logs de Acciones'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['usuario', 'timestamp']),
            models.Index(fields=['accion', 'timestamp']),
        ]

    def __str__(self):
        return f'{self.usuario} — {self.get_accion_display()} ({self.timestamp:%d/%m/%Y %H:%M})'



