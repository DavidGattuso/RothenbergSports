# api_camisetas/urls.py
from django.urls import path
from .views import ProductoListView

urlpatterns = [
    path('productos/', ProductoListView.as_view(), name='productos_list'),  # Vista para listar los productos
]