from django.shortcuts import render, redirect
from django.views.generic import  TemplateView, ListView
from django.contrib import messages
from datetime import date
from .models import Acciones_accionista, Datos_Accionista, Temp_Acciones_accionista, Temp_Datos_Accionista
# Create your views here.

class Index(TemplateView):
    template_name = "acciones/Index.html"

class Crear_Accionista(TemplateView):
    template_name = "acciones/Nuevo_Accionista.html"

    def validar_datos(self,request):
        id = request.POST['Identidad']
        if len(id) != 13:
            messages.error(request, "Error en Identidad", "Debe medir 13")
            return False
        list= Datos_Accionista.objects.filter(Identidad=id).count()
        if list>0:
            messages.error(request, "Ya existe un accionista con esa identidad", "Ya existe")
            return  False
        return  True

    def post(self, request, *args, **kwargs):
        va = self.validar_datos(request)
        if va == False:

            return render(request, "acciones/Nuevo_Accionista.html")
        else:
            Temp_Datos_Accionista.objects.filter(Usuario=request.user.username).delete()
            Temp_Acciones_accionista.objects.filter(Usuario=request.user.username).delete()
            A1 = Temp_Datos_Accionista(
                Nombre= request.POST['Cliente'],
                Identidad=request.POST['Identidad'],
                Fecha_Ingreso=request.POST['Fecha Ingreso'],
                Fundador=request.POST['Fundador'],
                Usuario= request.user.username

            )
            A1.save()

            Tipo_Accion = request.POST['Tipo_Apo']

            if Tipo_Accion=="reglamento":
                A2 = Temp_Acciones_accionista(
                    Usuario= request.user.username,
                    Fecha= date.today(),
                    Num_Recibo=int(request.POST['Núm. Recibo']),
                    Identidad= request.POST['Identidad'],
                    Reglamento= float(request.POST['Déposito Inicial']),
                    Extaordinaria=0.0,
                    Utilidad=0.0,
                    Donación=0.0,
                    Intereses=0.0,
                    Perdidas=0.0,
                    Total=float(request.POST['Déposito Inicial'])
                )
                A2.save()
            if Tipo_Accion=="donación":
                A2 = Temp_Acciones_accionista(
                    Usuario= request.user.username,
                    Fecha= date.today(),
                    Num_Recibo=int(request.POST['Núm. Recibo']),
                    Identidad= request.POST['Identidad'],
                    Reglamento= 0.0,
                    Extaordinaria=0.0,
                    Utilidad=0.0,
                    Donación=float(request.POST['Déposito Inicial']),
                    Intereses=0.0,
                    Perdidas=0.0,
                    Total=float(request.POST['Déposito Inicial'])
                )
                A2.save()

            if Tipo_Accion=="extraordinaria":
                A2 = Temp_Acciones_accionista(
                    Usuario= request.user.username,
                    Fecha= date.today(),
                    Num_Recibo=int(request.POST['Núm. Recibo']),
                    Identidad= request.POST['Identidad'],
                    Reglamento= 0.0,
                    Extaordinaria=float(request.POST['Déposito Inicial']),
                    Utilidad=0.0,
                    Donación=0.0,
                    Intereses=0.0,
                    Perdidas=0.0,
                    Total=float(request.POST['Déposito Inicial'])
                )
                A2.save()

        return redirect("acciones:mostrar_temp")

class Mostrar_temp(ListView):
    template_name ="acciones/Accionista_Mostrar.html"
    model = Temp_Acciones_accionista


    def get_context_data(self, *, object_list=None, **kwargs):
        ctx =super().get_context_data()
        datos = Temp_Datos_Accionista.objects.get(Usuario=self.request.user.username)

        ctx.update({
            'Cliente': datos.Nombre,
            'Identidad': datos.Identidad,
            'Fecha_Ingreso': datos.Fecha_Ingreso,
            'Fundador': datos.Fundador
        })
        return ctx
    def get_queryset(self):
        return Temp_Acciones_accionista.objects.filter(Usuario=self.request.user.username)
