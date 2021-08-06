
from django.urls import path

from .views import  LogoutView, UserLoginView, Paso


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
    path("profile/", Paso.as_view()),
    #path("profile/librodiario/", Cargar()),


]