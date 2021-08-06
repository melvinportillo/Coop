
from django.urls import path

from .views import   Paso


app_name = 'prestamos'

urlpatterns = [
    path(
        "prestamos/", Paso.as_view(),
        name="prestamos"
    ),


]