from django import forms
from .models import Postulante, DatosAcademicos, DatosSocioeconomicos


WIDGET_TEXT = lambda ph='': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ph})
WIDGET_NUM  = lambda ph='': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ph})
WIDGET_SEL  = lambda: forms.Select(attrs={'class': 'form-select'})
WIDGET_CHECK = lambda: forms.CheckboxInput(attrs={'class': 'form-check-input'})
WIDGET_DATE  = lambda: forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})


class DatosPersonalesForm(forms.ModelForm):
    class Meta:
        model = Postulante
        fields = ('nombre_completo', 'cedula', 'telefono', 'direccion', 'fecha_nacimiento')
        widgets = {
            'nombre_completo': WIDGET_TEXT('Ej: Juan Carlos García'),
            'cedula':          WIDGET_TEXT('Ej: 1234567890'),
            'telefono':        WIDGET_TEXT('Ej: 3001234567'),
            'direccion':       forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'fecha_nacimiento': WIDGET_DATE(),
        }
        labels = {
            'nombre_completo': 'Nombre completo',
            'cedula':          'Cédula de identidad',
            'telefono':        'Teléfono de contacto',
            'direccion':       'Dirección de residencia',
            'fecha_nacimiento': 'Fecha de nacimiento',
        }

    def clean_cedula(self):
        cedula = self.cleaned_data['cedula']
        qs = Postulante.objects.filter(cedula=cedula)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Esta cédula ya está registrada en el sistema.')
        return cedula


class DatosAcademicosForm(forms.ModelForm):
    class Meta:
        model = DatosAcademicos
        fields = ('institucion', 'carrera', 'semestre', 'promedio', 'creditos_aprobados', 'creditos_totales')
        widgets = {
            'institucion':        WIDGET_TEXT('Ej: Universidad Nacional'),
            'carrera':            WIDGET_TEXT('Ej: Ingeniería de Sistemas'),
            'semestre':           WIDGET_NUM('1–12'),
            'promedio':           WIDGET_NUM('0.00 – 5.00'),
            'creditos_aprobados': WIDGET_NUM('Ej: 90'),
            'creditos_totales':   WIDGET_NUM('Ej: 160'),
        }
        labels = {
            'institucion':        'Institución educativa',
            'carrera':            'Programa/Carrera',
            'semestre':           'Semestre actual',
            'promedio':           'Promedio acumulado (escala 0–5)',
            'creditos_aprobados': 'Créditos aprobados',
            'creditos_totales':   'Créditos totales del programa',
        }

    def clean_promedio(self):
        promedio = self.cleaned_data['promedio']
        if not (0 <= promedio <= 5):
            raise forms.ValidationError('El promedio debe estar entre 0 y 5.')
        return promedio


class DatosSocioeconomicosForm(forms.ModelForm):
    class Meta:
        model = DatosSocioeconomicos
        fields = (
            'ingreso_familiar', 'estrato', 'num_hermanos_universidad',
            'tipo_vivienda', 'trabaja', 'numero_personas_hogar', 'es_cabeza_hogar',
        )
        widgets = {
            'ingreso_familiar':         WIDGET_NUM('Ej: 1500000'),
            'estrato':                  WIDGET_SEL(),
            'num_hermanos_universidad': WIDGET_NUM('0, 1, 2…'),
            'tipo_vivienda':            WIDGET_SEL(),
            'trabaja':                  WIDGET_CHECK(),
            'numero_personas_hogar':    WIDGET_NUM('Ej: 4'),
            'es_cabeza_hogar':          WIDGET_CHECK(),
        }
        labels = {
            'ingreso_familiar':         'Ingreso familiar mensual (COP $)',
            'estrato':                  'Estrato socioeconómico',
            'num_hermanos_universidad': 'Hermanos estudiando en universidad',
            'tipo_vivienda':            'Tipo de vivienda',
            'trabaja':                  '¿Trabaja actualmente?',
            'numero_personas_hogar':    'Personas en el hogar',
            'es_cabeza_hogar':          '¿Es usted cabeza de hogar?',
        }

    def clean_ingreso_familiar(self):
        ingreso = self.cleaned_data['ingreso_familiar']
        if ingreso < 0:
            raise forms.ValidationError('El ingreso no puede ser negativo.')
        return ingreso


class EditarPostulanteStaffForm(forms.ModelForm):
    """Para que el evaluador edite datos de un postulante (con auditoría)."""
    class Meta:
        model = Postulante
        fields = ('nombre_completo', 'cedula', 'telefono', 'direccion')
        widgets = {
            'nombre_completo': WIDGET_TEXT(),
            'cedula':          WIDGET_TEXT(),
            'telefono':        WIDGET_TEXT(),
            'direccion':       forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
