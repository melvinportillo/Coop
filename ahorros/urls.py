from django.urls import path, include
from .views import Index, Crear_Cuenta, Mostrar_Temp, generar_pdf, Buscar_Ahorrante, guardar
from .views import Mostrar_Temp_1
app_name = 'ahorros'
urlpatterns = [
    path('index/',Index.as_view(), name='index'),
    path('nuevo',Crear_Cuenta.as_view(), name='nuevo'),
    path('mostrar_temp/',Mostrar_Temp.as_view(),name='mostrar_temp'),
    path('imprimir/', generar_pdf.as_view(),name='imprimir'),
    path('guardar/',guardar, name ='guardar'),
    path('buscar/', Buscar_Ahorrante.as_view(), name= 'buscar' ),
    path('mostrar_temp_1/',Mostrar_Temp_1.as_view(),name='mostrar_temp_1'),
]