from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Página principal de la tienda
    path('', views.index, name='index'),

    # Rutas para categorías específicas de camisetas
    path('hombre/', views.hombre_index, name='hombre_index'),
    path('mujer/', views.mujer_index, name='mujer_index'),
    path('ninos/', views.ninos_index, name='ninos_index'),

    # Detalle de producto específico
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),

    # Rutas de autenticación
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),

    # Funcionalidades del carrito de compras
    path('agregar-al-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),

    # Cerrar sesión del usuario
    path('logout/', views.logout_view, name='logout'),  # Usa tu vista personalizada

    # Vista de perfil de usuario y gestión de perfil
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('perfil/actualizar/', views.actualizar_perfil, name='actualizar_perfil'),
    path('perfil/eliminar/', views.eliminar_cuenta, name='eliminar_cuenta'),

    # Manejo de cantidades de productos en el carrito
    path('incrementar-cantidad/<int:item_id>/', views.incrementar_cantidad, name='incrementar_cantidad'),
    path('decrementar-cantidad/<int:item_id>/', views.decrementar_cantidad, name='decrementar_cantidad'),
    path('eliminar-item-carrito/<int:item_id>/', views.eliminar_item_carrito, name='eliminar_item_carrito'),

    # Ruta de búsqueda de productos
    path('buscar/', views.buscar, name='buscar'),

]