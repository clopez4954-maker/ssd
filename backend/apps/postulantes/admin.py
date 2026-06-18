from django.contrib import admin
from .models import Postulante, FichaSocioeconomica, DatosAcademicos, SolicitudBeca, MiembroFamiliar, MateriaSemestre

class FichaSocioeconomicaInline(admin.StackedInline):
    model = FichaSocioeconomica
    extra = 0

class DatosAcademicosInline(admin.StackedInline):
    model = DatosAcademicos
    extra = 0

class SolicitudBecaInline(admin.StackedInline):
    model = SolicitudBeca
    extra = 0

class MateriaSemestreInline(admin.TabularInline):
    model = MateriaSemestre
    extra = 0

@admin.register(Postulante)
class PostulanteAdmin(admin.ModelAdmin):
    list_display = ('user', 'cedula', 'ficha_completada')
    search_fields = ('cedula', 'user__username', 'user__first_name', 'user__last_name')
    inlines = [DatosAcademicosInline, FichaSocioeconomicaInline, SolicitudBecaInline, MateriaSemestreInline]

@admin.register(DatosAcademicos)
class DatosAcademicosAdmin(admin.ModelAdmin):
    list_display = ('postulante', 'ppa', 'materias_aprobadas', 'certificado_notas_pdf')

@admin.register(FichaSocioeconomica)
class FichaSocioeconomicaAdmin(admin.ModelAdmin):
    list_display = ('postulante', 'dependencia', 'ocupacion', 'rango_ingresos', 'fecha_llenado')

@admin.register(SolicitudBeca)
class SolicitudBecaAdmin(admin.ModelAdmin):
    list_display = ('postulante', 'puntaje_total', 'puntaje_academico', 'puntaje_socioeconomico', 'estado', 'fecha_asignacion')
    list_filter = ('estado',)

@admin.register(MateriaSemestre)
class MateriaSemestreAdmin(admin.ModelAdmin):
    list_display = ('postulante', 'sigla', 'nombre', 'nota', 'semestre')
    list_filter = ('semestre',)


