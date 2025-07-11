from django.db import models
from django.contrib.auth.models import User

# Perfil de usuario, asociado a un usuario específico
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username

# Categoría de productos
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

# Modelo local (NO lo usas si solo consumes la API, lo puedes borrar si quieres)
class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='img/')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    @property
    def precio_redondeado(self):
        return round(self.precio)

# Tallas locales (opcional si solo usas API)
class TallaProducto(models.Model):
    TALLAS_CHOICES = [
        ('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')
    ]
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="tallas_disponibles")
    talla = models.CharField(max_length=2, choices=TALLAS_CHOICES)

    def __str__(self):
        return f"{self.producto.nombre} - Talla {self.talla}"

# Carrito de compras
class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

# Ítems del carrito que referencian productos de la API (NO FK local)
class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto_id_externo = models.CharField(max_length=100)          # ID en la API externa
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)           # Descripción de la API
    imagen_url = models.URLField()                                  # URL de la imagen de la API
    precio = models.DecimalField(max_digits=10, decimal_places=2)   # Precio snapshot
    talla = models.CharField(max_length=10, blank=True, null=True)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.cantidad * self.precio

    def __str__(self):
        return f"{self.nombre} (x{self.cantidad}) - {self.talla or 'Sin talla'}"
