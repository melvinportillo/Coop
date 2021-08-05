from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model, login, logout
from django.views.generic import TemplateView, RedirectView
# Create your views here.


class UserLoginView(LoginView):
    template_name='usuarios/user_login.html'
    redirect_authenticated_user = True


class LogoutView(RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)