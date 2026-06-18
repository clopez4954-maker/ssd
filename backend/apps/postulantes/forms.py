from django import forms
from django.forms import inlineformset_factory
from .models import Postulante, FichaSocioeconomica, DatosAcademicos, MiembroFamiliar

class DatosAcademicosForm(forms.ModelForm):
    class Meta:
        model = DatosAcademicos
        fields = ('ppa', 'materias_aprobadas')
        widgets = {
            'ppa': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100', 'step': '0.01', 'placeholder': 'Ej. 85.5'}),
            'materias_aprobadas': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': 'Ej. 5'}),
        }
        labels = {
            'ppa': 'Promedio Ponderado Acumulado (PPA)',
            'materias_aprobadas': 'Cantidad de Materias Aprobadas',
        }


class RegistroAcademicoForm(forms.ModelForm):
    class Meta:
        model = DatosAcademicos
        fields = ['certificado_notas_pdf']
        widgets = {
            'certificado_notas_pdf': forms.FileInput(attrs={'accept': '.pdf', 'class': 'form-control'})
        }
        labels = {
            'certificado_notas_pdf': 'Certificado de Notas Semestre Pasado (PDF)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.certificado_notas_pdf:
            self.fields['certificado_notas_pdf'].required = False
        else:
            self.fields['certificado_notas_pdf'].required = True
            self.fields['certificado_notas_pdf'].error_messages = {
                'required': 'Por favor, adjunta tu certificado de notas en formato PDF.'
            }


class FichaSocioeconomicaForm(forms.ModelForm):
    dependencia = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select'}), label="Dependencia Económica")
    ocupacion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Agricultor, Docente, Comerciante...'}), label="Tipo de Ocupación", required=True)
    rango_ingresos = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select'}), label="Rango de Ingresos")
    num_integrantes = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select'}), label="Número de Integrantes del Grupo Familiar")
    num_hijos = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select'}), label="Descendencia (hijos)")
    lugar_residencia = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select'}), label="Lugar de Residencia")
    tenencia_vivienda = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select'}), label="Tenencia de Vivienda")
    tipo_vivienda = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select'}), label="Tipo de Vivienda / Infraestructura")
    procedencia = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select'}), label="Lugar de Procedencia")

    archivo_boleta_inscripcion = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.pdf,image/*'}), label="Boleta de Inscripción *", required=True)
    archivo_historico_academico = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.pdf,image/*'}), label="Histórico Académico *", required=True)
    archivo_carnet_identidad = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.pdf,image/*'}), label="Carnet de Identidad *", required=True)

    class Meta:
        model = FichaSocioeconomica
        fields = (
            'dependencia', 'ocupacion', 'rango_ingresos', 'num_integrantes', 'num_hijos',
            'lugar_residencia', 'tenencia_vivienda', 'tipo_vivienda', 'procedencia',
            'otro_beneficio', 'descripcion_otro_beneficio',
            'doc_ocupacion', 'doc_ingresos', 'doc_vivienda',
            'archivo_boleta_inscripcion', 'archivo_historico_academico', 'archivo_carnet_identidad'
        )
        widgets = {
            'otro_beneficio': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'otro_beneficio'}),
            'descripcion_otro_beneficio': forms.TextInput(attrs={'class': 'form-control', 'id': 'descripcion_otro_beneficio', 'placeholder': 'Indique cuál beneficio'}),
            'doc_ocupacion': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'doc_ingresos': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'doc_vivienda': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'num_integrantes': 'Número de Integrantes Familiares',
            'num_hijos': 'Número de Hijos',
            'otro_beneficio': '¿Cuenta con otro beneficio universitario?',
            'descripcion_otro_beneficio': 'Descripción del otro beneficio',
            'doc_ocupacion': 'Respaldo de Ocupación (Opcional)',
            'doc_ingresos': 'Respaldo de Ingresos (Opcional)',
            'doc_vivienda': 'Respaldo de Vivienda (Opcional)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.parametros.models import OpcionSocioeconomica
        
        # Populate choices dynamically from the database
        for var_name in ['dependencia', 'rango_ingresos', 'num_integrantes', 'num_hijos', 'lugar_residencia', 'tenencia_vivienda', 'tipo_vivienda', 'procedencia']:
            opciones = OpcionSocioeconomica.objects.filter(variable=var_name)
            self.fields[var_name].choices = [(opt.opcion_texto, opt.opcion_texto) for opt in opciones]

        if self.instance and self.instance.pk:
            # Map existing integer values back to selected string options in the form
            # num_integrantes mapping
            num = self.instance.num_integrantes
            if num <= 1:
                self.fields['num_integrantes'].initial = "Hasta 1 miembro"
            elif num in (2, 3):
                self.fields['num_integrantes'].initial = "De 2 a 3 miembros"
            elif num == 4:
                self.fields['num_integrantes'].initial = "De 3 a 4 miembros"
            else:
                self.fields['num_integrantes'].initial = "Más de 4 miembros"

            # num_hijos mapping
            hijos = self.instance.num_hijos
            if hijos == 0:
                self.fields['num_hijos'].initial = "Sin hijos"
            elif hijos == 1:
                self.fields['num_hijos'].initial = "1 hijo"
            else:
                self.fields['num_hijos'].initial = "Más de 1 hijo"

        # If editing and files exist, don't require them again
        if self.instance and self.instance.pk:
            if self.instance.archivo_boleta_inscripcion:
                self.fields['archivo_boleta_inscripcion'].required = False
            if self.instance.archivo_historico_academico:
                self.fields['archivo_historico_academico'].required = False
            if self.instance.archivo_carnet_identidad:
                self.fields['archivo_carnet_identidad'].required = False

    def clean_num_integrantes(self):
        val = self.cleaned_data['num_integrantes']
        mapping = {
            "Hasta 1 miembro": 1,
            "De 2 a 3 miembros": 3,
            "De 3 a 4 miembros": 4,
            "Más de 4 miembros": 5,
        }
        return mapping.get(val, 1)

    def clean_num_hijos(self):
        val = self.cleaned_data['num_hijos']
        mapping = {
            "Sin hijos": 0,
            "1 hijo": 1,
            "Más de 1 hijo": 2,
        }
        return mapping.get(val, 0)




class MiembroFamiliarForm(forms.ModelForm):
    class Meta:
        model = MiembroFamiliar
        fields = ('nombre_completo', 'parentesco', 'edad', 'ocupacion', 'observacion')
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Juan Pérez'}),
            'parentesco': forms.Select(attrs={'class': 'form-select'}, choices=MiembroFamiliar.parentesco_choices),
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 15'}),
            'ocupacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Estudiante'}),
            'observacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional'}),
        }

MiembroFamiliarFormSet = inlineformset_factory(
    FichaSocioeconomica,
    MiembroFamiliar,
    form=MiembroFamiliarForm,
    extra=1,
    can_delete=True
)

class EditarPostulanteStaffForm(forms.ModelForm):
    class Meta:
        model = Postulante
        fields = ('nombre_completo', 'cedula', 'telefono', 'direccion')
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula':          forms.TextInput(attrs={'class': 'form-control'}),
            'telefono':        forms.TextInput(attrs={'class': 'form-control'}),
            'direccion':       forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
