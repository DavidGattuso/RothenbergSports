from django.db import models
from django.contrib.auth.models import User



# Modelo para el perfil de usuario, asociado a un usuario específico
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username


# Modelo para las categorías de productos, permite clasificar los productos
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


# Modelo para los productos, incluye detalles de precio e imagen
class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='img/')  # Ahora se guarda en `media/img/`
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    @property
    def precio_redondeado(self):
        return round(self.precio)
    


# Modelo para las tallas de los productos, con opciones predefinidas
class TallaProducto(models.Model):
    TALLAS_CHOICES = [
        ('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')
    ]
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="tallas_disponibles")
    talla = models.CharField(max_length=2, choices=TALLAS_CHOICES)

    def __str__(self):
        return f"{self.producto.nombre} - Talla {self.talla}"


# Modelo para el carrito de compras, gestionado por el usuario
class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"


# Modelo para los items dentro del carrito, vinculado a productos específicos
class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    talla = models.CharField(max_length=10, blank=True, null=True)  

    def subtotal(self):
        # Calcula el subtotal de cada ítem en el carrito
        return self.cantidad * self.producto.precio




