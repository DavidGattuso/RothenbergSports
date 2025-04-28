from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('panel-admin/', views.admin_dashboard, name='admin_dashboard'),
    path('panel-admin/eliminar-usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('panel-admin/crear-usuario/', views.crear_usuario, name='crear_usuario'),
    path('panel-admin/editar-usuario/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
]