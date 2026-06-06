from django.contrib import admin
from .models import Postulante, DatosAcademicos, DatosSocioeconomicos


class DatosAcademicosInline(admin.StackedInline):
    model = DatosAcademicos
    extra = 0


class DatosSocioeconomicosInline(admin.StackedInline):
    model = DatosSocioeconomicos
    extra = 0


@admin.register(Postulante)
class PostulanteAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'cedula', 'convocatoria', 'datos_completos', 'fecha_registro')
    list_filter = ('datos_completos', 'convocatoria')
    search_fields = ('nombre_completo', 'cedula', 'user__email')
    inlines = [DatosAcademicosInline, DatosSocioeconomicosInline]
    readonly_fields = ('fecha_registro',)
