from django.urls import path, include
from .views import Index, Nuevo_Accion, Mostrar_Caja, Filtrar_Caja

app_name = 'caja'
urlpatterns = [
    path('index/',Index.as_view(), name='index'),
    path('nuevo/',Nuevo_Accion.as_view(), name='nuevo'),
    path('mostrar/', Mostrar_Caja.as_view(),name='mostrar'),
    path('filtrar/', Filtrar_Caja.as_view(),name='filtrar'),
]