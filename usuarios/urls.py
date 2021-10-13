
from django.urls import path

from .views import  LogoutView, UserLoginView, Paso, Libro_Mayor_v, Balance_General_view
from .views import Estado_Resultado_view

app_name = 'usuarios'

urlpatterns = [
    path(
        "login/", UserLoginView.as_view(),
        name="user_login"
    ),
    path(
        "logout/", LogoutView.as_view(),
        name="user_logout"
    ),
    path("profile/", Paso.as_view(),name="Libro Diario"),
    path("libro_mayor", Libro_Mayor_v.as_view(), name='Libro_Mayor'),
    path("balance_general/", Balance_General_view.as_view(),name="Balance_General"),
    path("estado_resultado/", Estado_Resultado_view.as_view(), name="Estado_Resultado"),
]