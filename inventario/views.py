from django.shortcuts import render , redirect
from django.views.generic import  TemplateView, ListView
from prestamos.models import Variables_Generales
from django.contrib import  messages
from .models import Temp_Inventario, Inventario
from datetime import  date
# Create your views here.

class Index(TemplateView):
    template_name = "inventario/Index.html"
    Variables_Generales.objects.filter(variable="Inventario").delete()
    A1 = Variables_Generales(
        variable="Inventario",
        valor="0"
    )
    A1.save()

class Nuevo(TemplateView):
    template_name = "inventario/Nuevo Articulo.html"

    def Validacion(self,request):
        valor = request.POST['Valor']
        valor = str(valor)

        if valor.isdigit():
            valor= float(valor)
            if valor>0 :
                return True
            else:
                messages.error(request,"Erro en valor", "Error en valor")
                return False
        else:
            messages.error(request,"Error en valor", "Error en valor")
            return  False

    def post(self,request,*args,**kwargs):
        v=self.Validacion(request)
        if v==True:
            Temp_Inventario.objects.filter(Usuario=self.request.user.username).delete()
            A1 = Temp_Inventario(
                Usuario= self.request.user.username,
                Codigo= request.POST['Código'],
                Descripcion=request.POST['Descripción'],
                Fecha_Ingreso= request.POST['Fecha_1'],
                Valor= float(request.POST['Valor'])
            )
            A1.save()
            return  redirect("inventario:mostrar")
        else:
            return  render(request,"inventario/Nuevo Articulo.html")


class Mostrar(ListView):
    template_name = "inventario/Mostrar Articulos.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx  = super().get_context_data()
        ctx.update({
            'Fecha': date.today()
        })

        return ctx
    def get_queryset(self):
        return  Temp_Inventario.objects.filter(Usuario=self.request.user.username)

    def post(self,request, *args,**kwargs):
        Datos = Temp_Inventario.objects.get(Usuario=request.user.username)

        A1 = Inventario(
            Codigo= Datos.Codigo,
            Descripcion=Datos.Descripcion,
            Fecha_Ingreso=Datos.Fecha_Ingreso,
            Valor=Datos.Valor
        )
        A1.save()

        return  redirect("usuarios:Libro Diario")