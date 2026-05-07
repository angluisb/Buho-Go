from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    tipo = forms.ChoiceField(
        choices=[
            ('estudiante', 'Estudiante'),
            ('comercio',   'Comercio'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model  = Usuario
        fields = ['first_name', 'last_name', 'username', 'email', 'tipo', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu apellido'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'email':    forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class LoginForm(AuthenticationForm):
    """
    AuthenticationForm usa USERNAME_FIELD del modelo automáticamente,
    así que ya va a pedir email. Solo le damos estilo.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Correo electrónico'
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'tu@correo.com'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })