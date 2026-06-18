from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Convocatoria(models.Model):
    """Período de convocatoria para postulación a becas."""

    nombre = models.CharField(max_length=200, verbose_name='Nombre de la convocatoria')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    fecha_inicio = models.DateField(verbose_name='Fecha de inicio')
    fecha_fin = models.DateField(verbose_name='Fecha de cierre')
    activa = models.BooleanField(default=False, verbose_name='Activa')
    creada_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='convocatorias_creadas',
        verbose_name='Creada por',
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Convocatoria'
        verbose_name_plural = 'Convocatorias'
        ordering = ['-fecha_inicio']

    def __str__(self):
        return self.nombre

    @property
    def esta_abierta(self):
        """Retorna True si la convocatoria está activa y dentro del período."""
        hoy = timezone.now().date()
        return self.activa and self.fecha_inicio <= hoy <= self.fecha_fin

    @property
    def estado_display(self):
        if not self.activa:
            return 'Inactiva'
        hoy = timezone.now().date()
        if hoy < self.fecha_inicio:
            return 'Próxima'
        if hoy > self.fecha_fin:
            return 'Cerrada'
        return 'Abierta'
