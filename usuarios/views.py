from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model, login, logout
from django.views.generic import TemplateView, RedirectView, ListView
from core.models import Libro_Diario
from datetime import date
from django.shortcuts import render
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


class Paso(TemplateView):


    def get(self, request, *args, **kwargs):
        ob = Libro_Diario.objects.filter(Fecha=date.today())
        ctx = {
            'object_list': ob
        }
        return  render(request,'transactions/Libro_Diario.html',ctx)






