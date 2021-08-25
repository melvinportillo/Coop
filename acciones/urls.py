from django.urls import path, include
from .views import Index, Crear_Accionista, Mostrar_temp, generar_pdf, guardar, Buscar_Accionista
from .views import Mostrar_temp_1

app_name = 'acciones'

urlpatterns =[
    path('index/', Index.as_view(), name='index'),
    path('nuevo/', Crear_Accionista.as_view(), name='nuevo'),
    path('mostrar_temp/', Mostrar_temp.as_view(), name='mostrar_temp'),
    path('imprimir/' ,generar_pdf.as_view(),name= 'imprimir'),
    path('guardar/', guardar, name='guardar'),
    path('buscar/,', Buscar_Accionista.as_view(), name='buscar',),
    path('mostrar_temp_1/', Mostrar_temp_1.as_view(), name='mostrar_temp_1'),
]