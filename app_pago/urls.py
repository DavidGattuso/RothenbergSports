from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # Proceso de pago
    path('pago/', views.proceso_pago, name='pago'),

    # Detalles de un pedido específico
    path('pedido/detalles/<int:pedido_id>/', views.detalles_pedido, name='detalles_pedido'),
    path('pedido/boleta/<int:pedido_id>/', views.descargar_boleta, name='descargar_boleta'),

    ]