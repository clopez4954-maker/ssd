from django.contrib import admin
from .models import Convocatoria


@admin.register(Convocatoria)
class ConvocatoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'activa', 'estado_display')
    list_filter = ('activa',)
    search_fields = ('nombre',)
