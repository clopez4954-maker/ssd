from django.db import models
from django.contrib.auth.models import User
from apps.convocatorias.models import Convocatoria


class Postulante(models.Model):
    """Datos personales del postulante. Relación 1-1 con auth.User."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='postulante',
        verbose_name='Usuario',
    )
    cedula = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        verbose_name='Cédula de identidad',
    )
    nombre_completo = models.CharField(max_length=200, verbose_name='Nombre completo')
    telefono = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    direccion = models.TextField(blank=True, verbose_name='Dirección')
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
    convocatoria = models.ForeignKey(
        Convocatoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='postulantes',
        verbose_name='Convocatoria',
    )
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    datos_completos = models.BooleanField(default=False, verbose_name='Datos completos')

    class Meta:
        verbose_name = 'Postulante'
        verbose_name_plural = 'Postulantes'
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['cedula']),
        ]

    def __str__(self):
        return f'{self.nombre_completo} ({self.cedula})'

    @property
    def puede_editar(self):
        """El postulante puede editar si la convocatoria está abierta y no ha sido evaluado."""
        if not self.convocatoria or not self.convocatoria.esta_abierta:
            return False
        if hasattr(self, 'evaluacion') and self.evaluacion.estado not in ('pendiente',):
            return False
        return True


class DatosAcademicos(models.Model):
    """Información académica del postulante."""

    postulante = models.OneToOneField(
        Postulante,
        on_delete=models.CASCADE,
        related_name='datos_academicos',
        verbose_name='Postulante',
    )
    institucion = models.CharField(max_length=200, verbose_name='Institución educativa')
    carrera = models.CharField(max_length=200, verbose_name='Carrera')
    semestre = models.PositiveSmallIntegerField(verbose_name='Semestre actual')
    promedio = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        verbose_name='Promedio acumulado (0-5)',
    )
    creditos_aprobados = models.PositiveIntegerField(
        verbose_name='Créditos aprobados',
    )
    creditos_totales = models.PositiveIntegerField(
        default=0,
        verbose_name='Créditos totales del programa',
    )

    class Meta:
        verbose_name = 'Datos Académicos'
        verbose_name_plural = 'Datos Académicos'

    def __str__(self):
        return f'Académicos de {self.postulante.nombre_completo}'


class DatosSocioeconomicos(models.Model):
    """Información socioeconómica del postulante."""

    ESTRATO_CHOICES = [(i, f'Estrato {i}') for i in range(1, 7)]

    VIVIENDA_CHOICES = [
        ('propia', 'Propia'),
        ('arrendada', 'Arrendada'),
        ('familiar', 'Familiar'),
        ('otro', 'Otro'),
    ]

    postulante = models.OneToOneField(
        Postulante,
        on_delete=models.CASCADE,
        related_name='datos_socioeconomicos',
        verbose_name='Postulante',
    )
    ingreso_familiar = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Ingreso familiar mensual (COP)',
    )
    estrato = models.PositiveSmallIntegerField(
        choices=ESTRATO_CHOICES,
        verbose_name='Estrato socioeconómico',
    )
    num_hermanos_universidad = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Número de hermanos en universidad',
    )
    tipo_vivienda = models.CharField(
        max_length=20,
        choices=VIVIENDA_CHOICES,
        default='arrendada',
        verbose_name='Tipo de vivienda',
    )
    trabaja = models.BooleanField(default=False, verbose_name='¿Trabaja actualmente?')
    numero_personas_hogar = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Número de personas en el hogar',
    )
    es_cabeza_hogar = models.BooleanField(
        default=False,
        verbose_name='¿Es cabeza de hogar?',
    )

    class Meta:
        verbose_name = 'Datos Socioeconómicos'
        verbose_name_plural = 'Datos Socioeconómicos'

    def __str__(self):
        return f'Socioeconómicos de {self.postulante.nombre_completo}'
