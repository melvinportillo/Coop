from django.shortcuts import render, redirect
from django.views.generic import  TemplateView, ListView
from django.contrib import messages
from datetime import date
from .models import  Temp_Datos_Ahorrante, Temp_Datos_Acciones_Ahorro, Acciones_Ahorros, Datos_Ahorros
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
            Temp_Datos_Ahorrante.objects.all().delete()
            Temp_Datos_Acciones_Ahorro.objects.all().delete()
            A1 = Temp_Datos_Ahorrante(
                Identidad=request.POST['Identidad'],
                Nombre= request.POST['Cliente'],
                Beneficiarios= request.POST['Beneficiarios'],
                Observacions=request.POST['Observaciones'],

            )
            A1.save()
            A2 = Temp_Datos_Acciones_Ahorro(
                    Fecha= date.today(),
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
        info = Temp_Datos_Ahorrante.objects.all()
        pres = info[0]
        ctx.update({
            'Cliente': pres.Nombre,
            'Identidad': pres.Identidad,
            'Beneficiarios': pres.Beneficiarios,
            'Observaciones': pres.Observacions,
        })

        return ctx
    def get_queryset(self):
        return  Temp_Datos_Acciones_Ahorro.objects.all()
