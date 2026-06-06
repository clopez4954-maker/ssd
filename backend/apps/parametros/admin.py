from django.contrib import admin
from .models import ParametroBeca


@admin.register(ParametroBeca)
class ParametroBecaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'valor', 'vigente', 'modificado_por', 'fecha_modificacion')
    list_filter = ('vigente',)
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('fecha_modificacion',)
