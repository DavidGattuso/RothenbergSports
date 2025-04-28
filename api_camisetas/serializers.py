from rest_framework import serializers
from ecommerce_camisetas.models import Producto, TallaProducto

class TallaProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TallaProducto
        fields = ['talla']  # Solo queremos serializar la talla

class ProductoSerializer(serializers.ModelSerializer):
    tallas = TallaProductoSerializer(many=True, read_only=True)  # Campo anidado para tallas

    class Meta:
        model = Producto
        fields = '__all__'  # Serializa todos los campos del modelo Producto, incluyendo las tallas