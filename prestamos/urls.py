from django.urls import path, re_path

from .views import   Prestamos, mostra_prestamp, GeneratePdf, Inicio, Guardar, Buscar_Prestamo, ListaPrestamos, Prestamo_A_Pagar

from .views import GeneratePdf1
app_name = 'prestamos'

urlpatterns = [
    path("inicio/", Inicio.as_view(), name="inicio"),
    path("guardar/", Guardar, name = "guardar"),
    path("buscar/",Buscar_Prestamo,name="buscar"),
    path('buscar/persona/',ListaPrestamos.as_view()),
    path('buscar/persona/prestamo/', Prestamo_A_Pagar.as_view()),
    path(
        "prestamos/", Prestamos,
        name="prestamos"
    ),
    path("prestamos/mostrar/", mostra_prestamp.as_view()),
    path("pdf1/", GeneratePdf1.as_view(),
         name="pdf1"),
    path("pdf/", GeneratePdf.as_view(),
         name="pdf"),
]

