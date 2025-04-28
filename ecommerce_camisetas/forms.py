from django import forms
from .models import UserProfile
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
    # Formulario para registrar un nuevo usuario
    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'tucorreo@email.com',
            'class': 'form-control'
        })
    )
    first_name = forms.CharField(
        label='Nombre',
        max_length=150,
        validators=[RegexValidator(regex=r'^[a-zA-Z\s]+$', message="El nombre solo debe contener letras.")],
        widget=forms.TextInput(attrs={
            'placeholder': 'Tu nombre',
            'class': 'form-control'
        })
    )
    last_name = forms.CharField(
        label='Apellido',
        max_length=150,
        validators=[RegexValidator(regex=r'^[a-zA-Z\s]+$', message="El apellido solo debe contener letras.")],
        widget=forms.TextInput(attrs={
            'placeholder': 'Tu apellido',
            'class': 'form-control'
        })
    )
    phone = forms.CharField(
        label='Teléfono',
        max_length=10,
        validators=[
            RegexValidator(regex=r'^9\s\d{8}$', message="El formato debe ser 9 12345678"),
        ],
        widget=forms.TextInput(attrs={
            'placeholder': '9 12345678',
            'class': 'form-control'
        })
    )
    birth_date = forms.DateField(
        label='Fecha de Nacimiento',
        widget=forms.TextInput(attrs={
            'placeholder': 'DD/MM/AAAA',
            'class': 'form-control',
            'pattern': r'\d{2}/\d{2}/\d{4}'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Introduce una contraseña',
            'class': 'form-control'
        }),
        min_length=8,
        validators=[
            RegexValidator(regex=r'^(?=.*[A-Z])(?=.*\d)', message="Debe contener al menos una mayúscula y un número."),
        ]
    )
    password2 = forms.CharField(
        label='Repetir Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repite la contraseña',
            'class': 'form-control'
        })
    )

    def clean_email(self):
        # Validar si el correo ya está registrado
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email

    def clean(self):
        # Verificar que ambas contraseñas coincidan
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            self.add_error('password2', "Las contraseñas no coinciden.")

        return cleaned_data


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone']  # Solo incluye el campo phone del modelo UserProfile


