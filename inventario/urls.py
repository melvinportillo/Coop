from django.urls import path, include
from  .views import  Index, Nuevo, Mostrar
app_name = 'inventario'
urlpatterns = [
    path('/index', Index.as_view(), name="index"),
    path('/nuevo', Nuevo.as_view(),name = 'nuevo'),
    path('/mostrar', Mostrar.as_view(), name = 'mostrar'),
]