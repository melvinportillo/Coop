from django.urls import path, include
from .views import Index, Crear_Cuenta, Mostrar_Temp
app_name = 'ahorros'
urlpatterns = [
    path('index/',Index.as_view(), name='index'),
    path('nuevo',Crear_Cuenta.as_view(), name='nuevo'),
    path('mostrar_temp/',Mostrar_Temp.as_view(),name='mostrar_temp'),
]