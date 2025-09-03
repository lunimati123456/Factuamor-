"""
URL configuration for factuamor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
# from productos.views import index
from django.contrib.auth import views as auth_views
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('productos.urls', namespace='productos')),
    path('clientes/', include('clientes.urls', namespace='clientes')),
    path('factura/', include('factura.urls', namespace='factura')),
    
    # URLs para la gestión de usuarios y autenticación
    path('cuentas/', include('usuarios.urls', namespace='usuarios')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]

# Configuración para servir archivos de medios y estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'static'))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)