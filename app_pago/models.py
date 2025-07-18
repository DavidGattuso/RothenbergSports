from django.db import models
from django.contrib.auth.models import User
from ecommerce_camisetas.models import Producto
from datetime import timedelta, date

# Modelo para la dirección de envío del usuario en el pedido
class DireccionEnvio(models.Model):
    usuario   = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre    = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono  = models.CharField(max_length=15)
    direccion = models.CharField(max_length=255)
    rut       = models.CharField(max_length=10)               # RUT de 8 a 9 dígitos
    email     = models.EmailField(null=True, blank=True)      # Opcional

    def __str__(self):
        return f"{self.nombre} {self.apellidos} - {self.direccion}"


# Modelo para los pedidos, vinculado al usuario y a la dirección de envío
class Pedido(models.Model):
    usuario         = models.ForeignKey(User, on_delete=models.CASCADE)
    direccion_envio = models.ForeignKey(DireccionEnvio, on_delete=models.CASCADE, null=True)
    fecha_pedido    = models.DateTimeField(auto_now_add=True)
    opciones_entrega = models.CharField(max_length=255)
    monto_envio     = models.DecimalField(max_digits=10, decimal_places=2, default=3990)
    total           = models.DecimalField(max_digits=10, decimal_places=2)
    estado          = models.CharField(max_length=100, default='Preparando pedido')

    # Campo para almacenar el ID que asigne la API remota
    external_id     = models.IntegerField(
                          null=True,
                          blank=True,
                          help_text="ID del pedido en el sistema remoto"
                      )

    def estimar_entrega(self):
        # Calcula una fecha de entrega estimada excluyendo domingos
        hoy = date.today()
        entrega = hoy + timedelta(days=3)
        if entrega.weekday() == 6:  # Si cae domingo, pasa a lunes
            entrega += timedelta(days=1)
        return entrega

    def __str__(self):
        return f"Pedido #{self.pk} ({self.estado})"


# Modelo para los ítems dentro de cada pedido, vinculados a productos específicos
class PedidoItem(models.Model):
    pedido               = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto_id_externo  = models.CharField(max_length=100)
    nombre               = models.CharField(max_length=255)
    descripcion          = models.TextField(blank=True, null=True)
    imagen_url           = models.URLField()
    precio               = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad             = models.PositiveIntegerField(default=1)
    talla                = models.CharField(max_length=5, null=True, blank=True)

    @property
    def subtotal(self):
        return self.precio * self.cantidad

    def __str__(self):
        return f"{self.nombre} x{self.cantidad}"


# Modelo para los pagos de los pedidos, incluye información de la tarjeta y el método de pago
class Pago(models.Model):
    usuario          = models.ForeignKey(User, on_delete=models.CASCADE)
    pedido           = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    nombre_tarjeta   = models.CharField(max_length=100)
    numero_tarjeta   = models.CharField(max_length=16)   # 16 dígitos
    fecha_vencimiento = models.CharField(max_length=5)    # MM/AA
    cvv              = models.CharField(max_length=3)     # 3 dígitos
    metodo_pago      = models.CharField(
                           max_length=10,
                           choices=[('debito', 'Débito'), ('credito', 'Crédito')]
                       )
    procesado        = models.BooleanField(default=False)

    def __str__(self):
        return f"Pago de {self.usuario.username} - {self.metodo_pago}"
