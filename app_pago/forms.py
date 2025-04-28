from django import forms
from django.core.validators import RegexValidator
from .models import Pedido

class ProcesoPagoForm(forms.ModelForm):
    # Formulario de proceso de pago, incluyendo detalles de envío y pago
    direccion = forms.CharField(label='Dirección de Envío')  # Dirección para el envío del pedido
    nombre = forms.CharField(label='Nombre')  # Nombre del cliente
    apellidos = forms.CharField(label='Apellidos')  # Apellidos del cliente
    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'correo@example.com',
            'class': 'form-control'
        })
    )  # Correo electrónico del cliente
    telefono = forms.CharField(
        label='Teléfono',
        validators=[RegexValidator(regex=r'^[1-9]\s\d{8}$', message="Formato: X 12345678")],
        widget=forms.TextInput(attrs={
            'placeholder': '9 12345678',
            'class': 'form-control'
        })
    )  # Teléfono de contacto del cliente
    rut = forms.CharField(
        label='RUT',
        widget=forms.TextInput(attrs={
            'placeholder': '12345678-9',
            'class': 'form-control'
        })
    )  # RUT del cliente
    terminos = forms.BooleanField(label='Acepto los términos y condiciones')  # Aceptación de términos

    # Campos para detalles de pago
    metodo_pago = forms.ChoiceField(
        choices=[('debito', 'Débito'), ('credito', 'Crédito')],
        label='Método de Pago'
    )
    numero_tarjeta = forms.CharField(
        max_length=19,  # 16 dígitos + 3 espacios
        label='Número de Tarjeta',
        widget=forms.TextInput(attrs={
            'placeholder': 'XXXX XXXX XXXX XXXX',
            'class': 'form-control'
        })
    )  # Número de tarjeta de pago
    fecha_vencimiento = forms.CharField(
        label='Fecha de Vencimiento (MM/AA)',
        widget=forms.TextInput(attrs={
            'placeholder': 'MM/AA',
            'class': 'form-control'
        })
    )  # Fecha de vencimiento en formato MM/AA
    codigo_seguridad = forms.CharField(
        max_length=3,
        label='Código de Seguridad',
        widget=forms.TextInput(attrs={
            'placeholder': 'CVV',
            'class': 'form-control'
        })
    )  # Código de seguridad de la tarjeta (CVV)

    class Meta:
        model = Pedido
        fields = [
            'direccion', 'nombre', 'apellidos', 'email', 'telefono', 'rut', 'terminos',
            'metodo_pago', 'numero_tarjeta', 'fecha_vencimiento', 'codigo_seguridad'
        ]


class CustomDateField(forms.DateField):
    # Campo personalizado para modificar el formato de fecha en el proceso de pago
    def to_python(self, value):
        if value:
            value = value.replace("/", "-")
        return super().to_python(value)