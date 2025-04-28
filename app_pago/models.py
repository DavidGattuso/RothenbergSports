from django.db import models
from django.contrib.auth.models import User
from ecommerce_camisetas.models import Producto
from datetime import timedelta, date
# Create your models here.

# Modelo para la dirección de envío del usuario en el pedido
class DireccionEnvio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=255)
    rut = models.CharField(max_length=10)  # RUT de 8 a 9 dígitos
    email = models.EmailField(null=True, blank=True)  # Permite que este campo sea opcional

    def __str__(self):
        return f"{self.nombre} {self.apellidos} - {self.direccion}"

# Modelo para los pedidos, vinculado al usuario y a la dirección de envío
class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    direccion_envio = models.ForeignKey(DireccionEnvio, on_delete=models.CASCADE, null=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    opciones_entrega = models.CharField(max_length=255)
    monto_envio = models.DecimalField(max_digits=10, decimal_places=2, default=3990)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=100, default='Preparando pedido')  # Estado inicial

    def estimar_entrega(self):
        # Calcula una fecha de entrega estimada excluyendo domingos
        hoy = date.today()
        dias_entrega = 3
        entrega = hoy + timedelta(days=dias_entrega)
        if entrega.weekday() == 6:  # Si es domingo, se mueve a lunes
            entrega += timedelta(days=1)
        return entrega


# Modelo para los items dentro de cada pedido, vinculados a productos específicos
class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.PositiveIntegerField(default=1)
    talla = models.CharField(max_length=5, null=True, blank=True)  # Talla del producto

    def subtotal(self):
        # Calcula el subtotal de cada ítem en el pedido
        return self.cantidad * self.producto.precio


# Modelo para los pagos de los pedidos, incluye información de la tarjeta y el método de pago
class Pago(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    nombre_tarjeta = models.CharField(max_length=100)
    numero_tarjeta = models.CharField(max_length=16)  # 16 dígitos
    fecha_vencimiento = models.CharField(max_length=5)  # MM/AA
    cvv = models.CharField(max_length=3)  # 3 dígitos
    metodo_pago = models.CharField(max_length=10, choices=[('debito', 'Débito'), ('credito', 'Crédito')])
    procesado = models.BooleanField(default=False)

    def __str__(self):
        return f"Pago de {self.usuario.username} - {self.metodo_pago}"