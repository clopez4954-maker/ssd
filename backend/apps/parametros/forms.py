from django import forms
from .models import ParametroBeca


class ParametroBecaForm(forms.ModelForm):
    class Meta:
        model = ParametroBeca
        fields = ('nombre', 'valor', 'descripcion', 'vigente')
        widgets = {
            'nombre':      forms.TextInput(attrs={'class': 'form-control'}),
            'valor':       forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'vigente':     forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre':      'Nombre del parámetro',
            'valor':       'Valor',
            'descripcion': 'Descripción',
            'vigente':     'Vigente',
        }


class ObservacionEvaluacionForm(forms.Form):
    """Formulario para agregar observaciones manuales al evaluar."""
    observaciones = forms.CharField(
        required=False,
        label='Observaciones del evaluador',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Notas adicionales para este postulante…',
        }),
    )
