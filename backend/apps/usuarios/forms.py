from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PerfilUsuario


class RegistroPostulanteForm(UserCreationForm):
    """Formulario de registro para nuevos postulantes."""
    first_name = forms.CharField(
        max_length=100, label='Nombres',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Juan Carlos'})
    )
    last_name = forms.CharField(
        max_length=100, label='Apellidos',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: García López'})
    )
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # email como username
        if commit:
            user.save()
            PerfilUsuario.objects.create(user=user, rol=PerfilUsuario.ROL_POSTULANTE)
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
