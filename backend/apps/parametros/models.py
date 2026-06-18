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


class RangoPPS(models.Model):
    desde = models.FloatField(verbose_name='Desde (promedio)')
    hasta = models.FloatField(verbose_name='Hasta (promedio)')
    puntaje = models.IntegerField(verbose_name='Puntaje')

    class Meta:
        verbose_name = 'Rango de PPS'
        verbose_name_plural = 'Rangos de PPS'
        ordering = ['desde']

    def __str__(self):
        return f'{self.desde} - {self.hasta} : {self.puntaje} pts'


class RangoMaterias(models.Model):
    desde = models.IntegerField(verbose_name='Desde (materias)')
    hasta = models.IntegerField(null=True, blank=True, verbose_name='Hasta (materias)', help_text='Dejar vacío para representar infinito / "o más"')
    puntaje = models.IntegerField(verbose_name='Puntaje')

    class Meta:
        verbose_name = 'Rango de Materias'
        verbose_name_plural = 'Rangos de Materias'
        ordering = ['desde']

    def __str__(self):
        hasta_str = f'{self.hasta}' if self.hasta is not None else 'o más'
        return f'{self.desde} - {hasta_str} : {self.puntaje} pts'


class OpcionSocioeconomica(models.Model):
    VARIABLE_CHOICES = [
        ('dependencia', 'Dependencia Económica (X1)'),
        ('ocupacion', 'Tipo de Ocupación (X2)'),
        ('rango_ingresos', 'Rango de Ingresos (X3)'),
        ('num_integrantes', 'Número de Integrantes (X4)'),
        ('num_hijos', 'Número de Hijos (X5)'),
        ('lugar_residencia', 'Lugar de Residencia (X6)'),
        ('tenencia_vivienda', 'Tenencia de Vivienda (X7)'),
        ('tipo_vivienda', 'Tipo de Vivienda (X8)'),
        ('procedencia', 'Lugar de Procedencia (X9)'),
    ]

    variable = models.CharField(max_length=50, choices=VARIABLE_CHOICES, verbose_name='Variable')
    opcion_texto = models.CharField(max_length=200, verbose_name='Texto de la Opción')
    puntaje = models.IntegerField(default=0, verbose_name='Puntaje')

    class Meta:
        verbose_name = 'Opción Socioeconómica'
        verbose_name_plural = 'Opciones Socioeconómicas'
        unique_together = ('variable', 'opcion_texto')
        ordering = ['variable', '-puntaje']

    def __str__(self):
        return f'[{self.get_variable_display()}] {self.opcion_texto} = {self.puntaje} pts'


class ReglaDesempate(models.Model):
    DIRECCION_CHOICES = [
        ('asc', 'Ascendente'),
        ('desc', 'Descendente'),
    ]

    nombre = models.CharField(max_length=100, verbose_name='Nombre de la Regla')
    campo_modelo = models.CharField(max_length=100, verbose_name='Campo de la Ficha/Postulante/Solicitud')
    orden_ejecucion = models.PositiveIntegerField(default=1, verbose_name='Orden de Ejecución')
    direccion = models.CharField(max_length=10, choices=DIRECCION_CHOICES, default='desc', verbose_name='Dirección')
    activo = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        verbose_name = 'Regla de Desempate'
        verbose_name_plural = 'Reglas de Desempate'
        ordering = ['orden_ejecucion']

    def __str__(self):
        return f'{self.orden_ejecucion}. {self.nombre} ({self.campo_modelo} {self.direccion})'

