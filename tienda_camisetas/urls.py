"""tienda_camisetas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),   # Acceso al admin
    path('', include('ecommerce_camisetas.urls')),  # URLs de ecommerce_camisetas
    path('app_pago/', include('app_pago.urls')),    # URLs de app_pago
    path('api/', include('api_camisetas.urls')),  # Incluye las rutas de la app api_camisetas
    path('panel-admin/', include('app_admin.urls')),  # Rutas personalizadas para admin
]

# Añadir ruta de media para desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)