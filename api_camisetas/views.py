from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ecommerce_camisetas.models import Producto, TallaProducto
from .serializers import ProductoSerializer
import json

class ProductoListView(APIView):
    def get(self, request, format=None):
        # Obtener todos los productos
        productos = Producto.objects.all()
        # Serializar los productos
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # Recibir los datos enviados
        serializer = ProductoSerializer(data=request.data)
        
        if serializer.is_valid():
            # Guardar el nuevo producto
            producto = serializer.save()

            # Obtener las tallas de la solicitud (las tallas vienen como un array)
            tallas_seleccionadas = request.data.get('tallas', [])

            # Si las tallas no vienen en el formato esperado (una lista), intentar convertirlas
            if isinstance(tallas_seleccionadas, str):
                try:
                    tallas_seleccionadas = json.loads(tallas_seleccionadas)
                except ValueError:
                    return Response({"error": "Formato de tallas incorrecto"}, status=status.HTTP_400_BAD_REQUEST)

            # Si no se seleccionan tallas, usar las predeterminadas
            if not tallas_seleccionadas:
                tallas_seleccionadas = ['XS', 'S', 'M', 'L', 'XL']

            # Crear o asociar tallas al producto
            for talla in tallas_seleccionadas:
                TallaProducto.objects.get_or_create(producto=producto, talla=talla)

            # Responder con los datos del producto creado
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Si hay errores en los datos, devolverlos
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)