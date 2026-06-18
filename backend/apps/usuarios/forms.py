from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PerfilUsuario


class RegistroPostulanteForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label="Nombres", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Juan Carlos'}))
    last_name = forms.CharField(max_length=150, required=True, label="Apellidos", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Pérez García'}))
    email = forms.EmailField(required=False, label="Correo Electrónico (opcional)", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}))
    telefono = forms.CharField(max_length=15, required=True, label="Celular", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 71234567'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {
            'username': 'Número de Registro Universitario',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 202412345'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.setdefault('class', 'form-control')
            if 'password' in name:
                field.widget.attrs['placeholder'] = '••••••••'
                field.widget.attrs['autocomplete'] = 'new-password'
            else:
                field.widget.attrs['autocomplete'] = 'off'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario registrado con este correo electrónico.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ya existe un usuario registrado con este número de registro.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data.get('email', '')
        if commit:
            user.save()
            PerfilUsuario.objects.get_or_create(user=user, defaults={'rol': PerfilUsuario.ROL_POSTULANTE})
            
            from apps.postulantes.models import Postulante
            postulante, created = Postulante.objects.get_or_create(user=user)
            postulante.cedula = user.username
            postulante.telefono = self.cleaned_data['telefono']
            postulante.nombre_completo = f"{user.first_name} {user.last_name}"
            postulante.save()
        return user


class CrearUsuarioStaffForm(forms.ModelForm):
    """Formulario para que el admin cree evaluadores."""
    password = forms.CharField(
        label='Contraseña temporal',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    rol = forms.ChoiceField(
        choices=[
            (PerfilUsuario.ROL_EVALUADOR, 'Evaluador'),
            (PerfilUsuario.ROL_ADMINISTRADOR, 'Administrador'),
        ],
        label='Rol',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.is_staff = True
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            rol = self.cleaned_data['rol']
            es_admin = rol == PerfilUsuario.ROL_ADMINISTRADOR
            PerfilUsuario.objects.create(user=user, rol=rol)
            if es_admin:
                user.is_superuser = True
                user.save()
        return user


class EditarUsuarioForm(forms.ModelForm):
    """Editar datos de un usuario staff existente."""
    rol = forms.ChoiceField(
        choices=PerfilUsuario.ROL_CHOICES,
        label='Rol',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_active')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'is_active': 'Usuario activo',
        }
