from django.contrib import admin
from .models import Pedido, DireccionEnvio, PedidoItem, Pago

# Personalización de la vista de Pedido en el admin
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'get_direccion', 'fecha_pedido', 'total', 'opciones_entrega')
    search_fields = ('usuario__username',)
    list_filter = ('fecha_pedido',)  # Filtro por fecha de pedido

    def get_direccion(self, obj):
        # Método para acceder a la dirección de envío del pedido
        return obj.direccion_envio.direccion
    get_direccion.short_description = 'Dirección de Envío'  # Nombre visible en la columna del admin

# Registramos los modelos en el admin con sus configuraciones personalizadas
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(DireccionEnvio)
admin.site.register(PedidoItem)
admin.site.register(Pago)