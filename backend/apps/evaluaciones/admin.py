from django.contrib import admin
from .models import Evaluacion


@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = (
        'postulante', 'estado', 'puntaje_total',
        'puntaje_academico', 'puntaje_socioeconomico',
        'evaluado_por', 'fecha_evaluacion',
    )
    list_filter = ('estado', 'convocatoria')
    search_fields = ('postulante__nombre_completo', 'postulante__cedula')
    readonly_fields = ('fecha_evaluacion',)
