from django.urls import path

from .views import   Prestamos, mostra_prestamp, GeneratePdf


app_name = 'prestamos'

urlpatterns = [
    path(
        "prestamos/", Prestamos,
        name="prestamos"
    ),
    path("prestamos/mostrar/", mostra_prestamp.as_view()),
    path("pdf/", GeneratePdf.as_view(),
         name="pdf"),
]