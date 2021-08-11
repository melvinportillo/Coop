from django.urls import path

from .views import   Prestamos, mostra_prestamp, GeneratePdf, Inicio, Guardar


app_name = 'prestamos'

urlpatterns = [
    path("inicio/", Inicio.as_view(), name="inicio"),
    path("guardar/", Guardar, name = "guardar"),
    path(
        "prestamos/", Prestamos,
        name="prestamos"
    ),
    path("prestamos/mostrar/", mostra_prestamp.as_view()),
    path("pdf/", GeneratePdf.as_view(),
         name="pdf"),
]