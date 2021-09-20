from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model, login, logout
from django.views.generic import TemplateView, RedirectView, ListView
from core.models import Libro_Diario, Libro_Mayor
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

    def post(self,request,*args,**kwargs):
        fecha = request.POST['Fecha_1']
        ob = Libro_Diario.objects.filter(Fecha=fecha)
        ctx={
            'object_list': ob
        }
        return render(request, 'transactions/Libro_Diario.html', ctx)



class Libro_Mayor_v(TemplateView):

    def get(self, request, *args, **kwargs):
        opciones_cuentas=Libro_Mayor.objects.order_by('Cuenta').values_list('Cuenta', flat=True).distinct()
        ctx={
            'opciones':opciones_cuentas
        }
        return  render(request,"transactions/Libro Mayor.html",ctx)

    def post(self, request,*args,**kwargs):
        opciones_cuentas = Libro_Mayor.objects.order_by('Cuenta').values_list('Cuenta', flat=True).distinct()
        Cuenta = request.POST['Cuenta']
        Fecha_i= request.POST['Fecha_1']
        Fecha_f = request.POST['Fecha_2']
        ob= Libro_Mayor.objects.filter(Fecha__gte=Fecha_i, Fecha__lte=Fecha_f, Cuenta=Cuenta)
        ctx={
            'opciones': opciones_cuentas,
            'object_list': ob,
            'Cuenta':Cuenta,
        }
        return  render(request,'transactions/Libro Mayor.html',ctx)
