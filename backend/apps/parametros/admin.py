from django.contrib import admin
from .models import ParametroBeca, RangoPPS, RangoMaterias, OpcionSocioeconomica, ReglaDesempate


@admin.register(ParametroBeca)
class ParametroBecaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'valor', 'vigente', 'modificado_por', 'fecha_modificacion')
    list_filter = ('vigente',)
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('fecha_modificacion',)


@admin.register(RangoPPS)
class RangoPPSAdmin(admin.ModelAdmin):
    list_display = ('desde', 'hasta', 'puntaje')
    ordering = ('desde',)


@admin.register(RangoMaterias)
class RangoMateriasAdmin(admin.ModelAdmin):
    list_display = ('desde', 'hasta', 'puntaje')
    ordering = ('desde',)


@admin.register(OpcionSocioeconomica)
class OpcionSocioeconomicaAdmin(admin.ModelAdmin):
    list_display = ('variable', 'opcion_texto', 'puntaje')
    list_filter = ('variable',)
    search_fields = ('opcion_texto',)
    ordering = ('variable', '-puntaje')


@admin.register(ReglaDesempate)
class ReglaDesempateAdmin(admin.ModelAdmin):
    list_display = ('id', 'orden_ejecucion', 'nombre', 'campo_modelo', 'direccion', 'activo')
    list_display_links = ('id', 'nombre')
    list_editable = ('orden_ejecucion', 'activo')
    ordering = ('orden_ejecucion',)


