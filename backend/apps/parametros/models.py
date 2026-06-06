from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class ParametroBeca(models.Model):
    """
    Parámetros configurables del modelo de evaluación de becas.
    Todos los valores son editables desde el panel de administración.
    """

    nombre = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name='Nombre del parámetro',
        help_text='Identificador único (ej: peso_academico)',
    )
    valor = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        verbose_name='Valor',
    )
    descripcion = models.TextField(verbose_name='Descripción', blank=True)
    vigente = models.BooleanField(default=True, verbose_name='Vigente')
    modificado_por = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='parametros_modificados',
        verbose_name='Modificado por',
    )
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name='Última modificación')

    class Meta:
        verbose_name = 'Parámetro de Beca'
        verbose_name_plural = 'Parámetros de Beca'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre} = {self.valor}'

    @classmethod
    def get_dict(cls):
        """Retorna todos los parámetros vigentes como diccionario {nombre: valor}."""
        return {p.nombre: float(p.valor) for p in cls.objects.filter(vigente=True)}
