from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from apps.convocatorias.models import Convocatoria


def validate_file_size(value):
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5 MB
        raise ValidationError("El archivo no puede superar los 5 MB.")


class Postulante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='postulante')
    cedula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15, blank=True, default='')
    ficha_completada = models.BooleanField(default=False)
    carrera = models.CharField(max_length=100, blank=True, default='')
    facultad = models.CharField(max_length=100, blank=True, default='Facultad Integral de los Valles Cruceños')
    
    # Mantener para compatibilidad
    nombre_completo = models.CharField(max_length=200, blank=True)
    direccion = models.TextField(blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    convocatoria = models.ForeignKey(Convocatoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='postulantes')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    datos_completos = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Postulante'
        verbose_name_plural = 'Postulantes'

    def __str__(self):
        return f'{self.user.get_full_name() or self.nombre_completo or self.user.username} ({self.cedula})'

    def get_estado_postulacion(self):
        try:
            ficha = self.ficha_socioeconomica
            ficha_completa = bool(
                ficha.dependencia and
                ficha.ocupacion and
                ficha.rango_ingresos and
                ficha.num_integrantes is not None and
                ficha.num_hijos is not None and
                ficha.lugar_residencia and
                ficha.tenencia_vivienda and
                ficha.tipo_vivienda and
                ficha.procedencia
            )
        except Exception:
            ficha_completa = False

        tiene_materias = self.materias.exists()

        progreso = 0
        if ficha_completa:
            progreso += 50
        if tiene_materias:
            progreso += 50

        is_completa = (ficha_completa and tiene_materias)

        return {
            'ficha_completa': ficha_completa,
            'tiene_materias': tiene_materias,
            'progreso': progreso,
            'is_completa': is_completa,
            'estado': 'completa' if is_completa else 'incompleta',
            'estado_display': 'Postulación Completada' if is_completa else 'Postulación en Proceso'
        }


class DatosAcademicos(models.Model):
    postulante = models.OneToOneField(Postulante, on_delete=models.CASCADE, related_name='datos_academicos')
    ppa = models.FloatField(help_text="Promedio Ponderado Acumulado (0-100)")
    materias_aprobadas = models.IntegerField()
    certificado_notas_pdf = models.FileField(
        upload_to='certificados/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf']), validate_file_size],
        blank=True,
        null=True,
        help_text="Certificado de notas del semestre pasado (PDF)"
    )
    puntaje_ppa = models.FloatField(default=0.0)
    puntaje_materias = models.FloatField(default=0.0)
    puntaje_academico_total = models.FloatField(default=0.0)

    class Meta:
        verbose_name = 'Datos Académicos'
        verbose_name_plural = 'Datos Académicos'

    def __str__(self):
        return f'Académico - {self.postulante.user.username} (PPA: {self.ppa})'


class MateriaSemestre(models.Model):
    postulante = models.ForeignKey(Postulante, on_delete=models.CASCADE, related_name='materias')
    nombre = models.CharField(max_length=100)
    sigla = models.CharField(max_length=10)
    nota = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    semestre = models.CharField(max_length=20, default='2025-1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Materia Cursada'
        verbose_name_plural = 'Materias Cursadas'
        ordering = ['semestre', 'sigla']

    def __str__(self):
        return f"{self.sigla} - {self.nombre} ({self.nota})"


from django.utils import timezone

class FichaSocioeconomica(models.Model):
    postulante = models.OneToOneField(Postulante, on_delete=models.CASCADE, related_name='ficha_socioeconomica')
    # X1 a X9 se almacenan como texto (la opción seleccionada)
    dependencia = models.CharField(max_length=100, null=True, blank=True)  # opción textual
    ocupacion = models.CharField(max_length=100, default='', help_text="Escribe tu ocupación o trabajo actual")
    rango_ingresos = models.CharField(max_length=100, null=True, blank=True)
    num_integrantes = models.IntegerField(default=1)
    num_hijos = models.IntegerField(default=0)
    lugar_residencia = models.CharField(max_length=100, null=True, blank=True)  # "hasta 2do anillo" / "fuera"
    tenencia_vivienda = models.CharField(max_length=100, null=True, blank=True)
    tipo_vivienda = models.CharField(max_length=100, null=True, blank=True)
    procedencia = models.CharField(max_length=100, null=True, blank=True)
    
    # adicionales
    otro_beneficio = models.BooleanField(default=False)
    descripcion_otro_beneficio = models.CharField(max_length=200, blank=True)
    
    # documentos de respaldo (opcionales)
    doc_ocupacion = models.FileField(upload_to='fichas/ocupacion/', blank=True)
    doc_ingresos = models.FileField(upload_to='fichas/ingresos/', blank=True)
    doc_vivienda = models.FileField(upload_to='fichas/vivienda/', blank=True)
    
    # Requisitos obligatorios
    archivo_boleta_inscripcion = models.FileField(upload_to='fichas/boletas/', blank=True, null=True)
    archivo_historico_academico = models.FileField(upload_to='fichas/historicos/', blank=True, null=True)
    archivo_carnet_identidad = models.FileField(upload_to='fichas/identidades/', blank=True, null=True)
    fecha_llenado = models.DateTimeField(default=timezone.now, blank=True)


    class Meta:
        verbose_name = 'Ficha Socioeconómica'
        verbose_name_plural = 'Fichas Socioeconómicas'

    def __str__(self):
        return f'Ficha de {self.postulante}'


class SolicitudBeca(models.Model):
    postulante = models.OneToOneField(Postulante, on_delete=models.CASCADE, related_name='solicitud_beca')
    puntaje_total = models.FloatField(null=True, blank=True)
    puntaje_academico = models.FloatField(null=True, blank=True)
    puntaje_socioeconomico = models.FloatField(null=True, blank=True)
    estado = models.CharField(max_length=50, default='Pendiente')  # 'Pendiente', 'Postulación completada', 'Beca Asignada', 'No seleccionado'
    fecha_asignacion = models.DateTimeField(null=True, blank=True)
    motivo_rechazo = models.TextField(blank=True, null=True)
    fecha_revision = models.DateTimeField(null=True, blank=True)
    observaciones_internas = models.TextField(blank=True, null=True)
    rechazado = models.BooleanField(default=False)
    fecha_rechazo = models.DateTimeField(null=True, blank=True)
    notificado_rechazo = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Solicitud de Beca'
        verbose_name_plural = 'Solicitudes de Beca'

    def __str__(self):
        return f'Solicitud de Beca - {self.postulante} ({self.estado})'


class MiembroFamiliar(models.Model):
    """Datos de cada miembro del grupo familiar."""
    ficha = models.ForeignKey(
        FichaSocioeconomica,
        on_delete=models.CASCADE,
        related_name='miembros_familiares'
    )
    nombre_completo = models.CharField(max_length=200, verbose_name='Nombre completo')
    parentesco = models.CharField(max_length=100, verbose_name='Parentesco')
    parentesco_choices = [
        ('padre', 'Padre'),
        ('madre', 'Madre'),
        ('hermano', 'Hermano/a'),
        ('hijo', 'Hijo/a'),
        ('esposo', 'Esposo/a / Pareja'),
        ('otro', 'Otro familiar'),
    ]
    edad = models.PositiveSmallIntegerField(verbose_name='Edad')
    ocupacion = models.CharField(max_length=200, verbose_name='Ocupación')
    observacion = models.CharField(max_length=255, blank=True, verbose_name='Observación')

    class Meta:
        verbose_name = 'Miembro Familiar'
        verbose_name_plural = 'Miembros Familiares'

    def __str__(self):
        return f'{self.nombre_completo} ({self.parentesco})'
