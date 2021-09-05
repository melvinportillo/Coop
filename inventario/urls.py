from django.urls import path, include
from  .views import  Index, Nuevo, Mostrar, Filtrar_Fecha, Filtrar_codigo
app_name = 'inventario'
urlpatterns = [
    path('index', Index.as_view(), name="index"),
    path('nuevo', Nuevo.as_view(),name = 'nuevo'),
    path('mostrar', Mostrar.as_view(), name = 'mostrar'),
    path('filtrar1', Filtrar_Fecha.as_view(),name='filtrar1'),
    path('filrar2', Filtrar_codigo.as_view(),name='filtrar2'),
]