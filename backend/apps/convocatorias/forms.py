from django import forms
from .models import Convocatoria


class ConvocatoriaForm(forms.ModelForm):
    class Meta:
        model = Convocatoria
        fields = ('nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'activa')
        widgets = {
            'nombre':      forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin':    forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'activa':       forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre':      'Nombre de la convocatoria',
            'descripcion': 'Descripción',
            'fecha_inicio': 'Fecha de inicio',
            'fecha_fin':    'Fecha de cierre',
            'activa':       'Activar convocatoria',
        }

    def clean(self):
        cleaned = super().clean()
        inicio = cleaned.get('fecha_inicio')
        fin = cleaned.get('fecha_fin')
        if inicio and fin and fin <= inicio:
            raise forms.ValidationError('La fecha de cierre debe ser posterior a la fecha de inicio.')
        return cleaned
