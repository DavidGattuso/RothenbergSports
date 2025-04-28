from django.contrib import admin
from .models import Producto, Carrito, CarritoItem, UserProfile, Categoria, TallaProducto


# Configuración para gestionar tallas dentro de la vista de Producto
class TallaProductoInline(admin.TabularInline):
    model = TallaProducto
    extra = 0  # No mostrar líneas adicionales

    # Sobrescribir el método para guardar las tallas automáticamente
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        producto = form.instance
        # Listado de tallas a agregar
        tallas = ['XS', 'S', 'M', 'L', 'XL']
        
        # Verificar si las tallas ya están creadas
        for talla in tallas:
            TallaProducto.objects.get_or_create(producto=producto, talla=talla)


# Personalización de la vista de Producto en el admin con el inline de tallas
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria')
    list_filter = ('categoria',)  # Filtro de categoría para facilitar búsqueda
    inlines = [TallaProductoInline]  # Añadir TallaProducto como inline de Producto


# Personalización de la vista de Categoría en el admin
admin.site.register(Categoria)


# Personalización de la vista de Carrito en el admin
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'total')
    search_fields = ('usuario__username',)  # Búsqueda por nombre de usuario


# Personalización de la vista de CarritoItem en el admin
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'producto', 'cantidad')
    search_fields = ('producto__nombre', 'carrito__usuario__username')  # Búsqueda avanzada


# Personalización de la vista de UserProfile en el admin
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'birth_date')
    search_fields = ('user__username', 'phone')  # Opciones de búsqueda para agilizar gestión


# Registramos los modelos en el admin con sus configuraciones personalizadas
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Carrito, CarritoAdmin)
admin.site.register(CarritoItem, CarritoItemAdmin)
admin.site.register(UserProfile, UserProfileAdmin)