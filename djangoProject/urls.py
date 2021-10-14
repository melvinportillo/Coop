"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from core.views import HomeView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('usuarios.urls', namespace='usuarios')),
    path('prestamos/', include('prestamos.urls', namespace='prestamos')),
    path('ahorros/', include('ahorros.urls', namespace='ahorros')),
    path('acciones/',include('acciones.urls',namespace='acciones')),
    path('caja/', include('caja.urls',namespace='caja')),
    path('inventario/',include('inventario.urls', namespace="inventario")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
