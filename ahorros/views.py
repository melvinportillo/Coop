from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import  TemplateView, ListView
from django.contrib import messages
from datetime import date
from django.views import View
from .models import  Temp_Datos_Ahorrante, Temp_Datos_Acciones_Ahorro, Acciones_Ahorros, Datos_Ahorros
from .utils import render_to_pdf
# Create your views here.

class Index(TemplateView):
    template_name= "ahorros/Index.html"


class Crear_Cuenta (TemplateView):
    template_name = "ahorros/Nuevo_Ahorrante.html"

    def validar_datos(self, request):
        identidad =  request.POST['Identidad']
        if len(identidad) != 13:
            messages.error(request, "Error en Identidad", "Debe medir 13")
            return False
        dep = float(request.POST['Déposito Inicial'])
        if dep<=0:
            messages.error(request, "Error en Déposito Inicial", "Debe medir 13")
            return False
        return True

    def post(self, request, *args, **kwargs):
        va = self.validar_datos(request)
        if va == False:
            c = {
                'Cliente': request.POST['Cliente'],
                'Identidad': request.POST['Identidad'],
                'Beneficiarios': request.POST['Beneficiarios'],
                'Observaciones': request.POST['Observaciones'],
                'Déposito Inicial': request.POST['Déposito Inicial']
            }
            return  render(request, "ahorros/Nuevo_Ahorrante.html",context=c)
        else:
            user= request.user.username
            Temp_Datos_Ahorrante.objects.filter(usuario=user).delete()
            Temp_Datos_Acciones_Ahorro.objects.filter(usuario=user).delete()
            A1 = Temp_Datos_Ahorrante(
                Identidad=request.POST['Identidad'],
                Nombre= request.POST['Cliente'],
                usuario=user,
                Beneficiarios= request.POST['Beneficiarios'],
                Observacions=request.POST['Observaciones'],

            )
            A1.save()
            A2 = Temp_Datos_Acciones_Ahorro(
                    Fecha= date.today(),
                    usuario=request.user.username,
                    Identidad= request.POST['Identidad'],
                    Num_Recibo=request.POST['Núm. Recibo'],
                    Deposito= float(request.POST['Déposito Inicial']),
                    Intereses= 0.0,
                    Retiro= 0.0,
                    Saldo= float(request.POST['Déposito Inicial']),

            )
            A2.save()

            return  redirect('ahorros:mostrar_temp')



class Mostrar_Temp(ListView):
    template_name = "ahorros/Ahorrante_mostrar.html"
    model = Temp_Datos_Acciones_Ahorro
    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        info = Temp_Datos_Ahorrante.objects.filter(usuario= self.request.user.username)
        pres = info[0]
        ctx.update({
            'Cliente': pres.Nombre,
            'Identidad': pres.Identidad,
            'Beneficiarios': pres.Beneficiarios,
            'Observaciones': pres.Observacions,
        })

        return ctx
    def get_queryset(self):
        user = self.request.user.username
        return  Temp_Datos_Acciones_Ahorro.objects.filter(usuario=user)


class generar_pdf(View):
    def get(self, request, *args, **kwargs):
        ob = Temp_Datos_Acciones_Ahorro.objects.filter(usuario=request.user.username)
        presta= Temp_Datos_Ahorrante.objects.filter(usuario=request.user.username)
        dato= presta[0]
        ctx = {
            'Cliente': dato.Nombre,
            'Identidad': dato.Identidad,
            'Beneficiarios': dato.Beneficiarios,
            'Observaciones': dato.Observacions,
            'object_list': ob
        }
        pdf= render_to_pdf('pdf/ahorros_mostrar.html',ctx)
        return HttpResponse(pdf, content_type='ahorros/pdf')

def guardar(request):
     datos = Temp_Datos_Ahorrante.objects.get(usuario=request.user.username)
     acciones = Temp_Datos_Acciones_Ahorro.objects.filter(usuario=request.user.username)

     A1 = Datos_Ahorros(
       Identidad= datos.Identidad,
       Nombre= datos.Nombre,
       Beneficiarios= datos.Beneficiarios,
       Observacions= datos.Observacions
     )
     A1.save()

     for accion in acciones:
         A2 = Acciones_Ahorros(
             Identidad= accion.Identidad,
             Fecha= accion.Fecha,
             Num_Recibo=accion.Num_Recibo,
             Deposito= accion.Deposito,
             Intereses=accion.Intereses,
             Retiro=accion.Retiro,
             Saldo=accion.Saldo
         )
         A2.save()
     return render(request,"transactions/Libro_Diario.html")
