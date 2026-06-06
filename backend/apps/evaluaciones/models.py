from django.db import models
from django.contrib.auth.models import User
from apps.postulantes.models import Postulante
from apps.convocatorias.models import Convocatoria


class Evaluacion(models.Model):
    """Resultado de la evaluación de un postulante."""

    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_EVALUADO = 'evaluado'
    ESTADO_APROBADO = 'aprobado'
    ESTADO_RECHAZADO = 'rechazado'

    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_EVALUADO, 'Evaluado'),
        (ESTADO_APROBADO, 'Aprobado'),
        (ESTADO_RECHAZADO, 'Rechazado'),
    ]

    postulante = models.OneToOneField(
        Postulante,
        on_delete=models.CASCADE,
        related_name='evaluacion',
        verbose_name='Postulante',
    )
    convocatoria = models.ForeignKey(
        Convocatoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evaluaciones',
        verbose_name='Convocatoria',
    )
    puntaje_academico = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        verbose_name='Puntaje académico',
    )
    puntaje_socioeconomico = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        verbose_name='Puntaje socioeconómico',
    )
    puntaje_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        verbose_name='Puntaje total',
        db_index=True,
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=ESTADO_PENDIENTE,
        db_index=True,
        verbose_name='Estado',
    )
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones del evaluador',
    )
    fecha_evaluacion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de evaluación',
    )
    evaluado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evaluaciones_realizadas',
        verbose_name='Evaluado por',
    )

    class Meta:
        verbose_name = 'Evaluación'
        verbose_name_plural = 'Evaluaciones'
        ordering = ['-puntaje_total']
        indexes = [
            models.Index(fields=['estado', 'puntaje_total']),
        ]

    def __str__(self):
        return f'Evaluación de {self.postulante.nombre_completo} — {self.get_estado_display()}'

    @property
    def estado_color(self):
        """Clase Bootstrap para el badge de estado."""
        colores = {
            self.ESTADO_PENDIENTE: 'secondary',
            self.ESTADO_EVALUADO: 'info',
            self.ESTADO_APROBADO: 'success',
            self.ESTADO_RECHAZADO: 'danger',
        }
        return colores.get(self.estado, 'secondary')
