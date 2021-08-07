from django.urls import path

from .views import   Prestamos


app_name = 'prestamos'

urlpatterns = [
    path(
        "prestamos/", Prestamos,
        name="prestamos"
    ),

]