
from django.urls import path

from .views import  LogoutView, UserLoginView


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

]