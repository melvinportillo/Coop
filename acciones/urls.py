from django.urls import path, include
from .views import Index, Crear_Accionista, Mostrar_temp, generar_pdf, guardar
app_name = 'acciones'

urlpatterns =[
    path('index/', Index.as_view(), name='index'),
    path('nuevo/', Crear_Accionista.as_view(), name='nuevo'),
    path('mostrar_temp/', Mostrar_temp.as_view(), name='mostrar_temp'),
    path('imprimir/' ,generar_pdf.as_view(),name= 'imprimir'),
    path('guardar/', guardar, name='guardar'),
]