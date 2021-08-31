from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib import  messages
from .models import Temp_Caja, Caja
from datetime import  date
from prestamos.models import Variables_Generales

# Create your views here.

class Index(TemplateView):
    template_name = "caja/index.html"
    Variables_Generales.objects.filter(variable="Caja").delete()
    A1=Variables_Generales(
       variable="Caja",
       valor="0"
    )
    A1.save()

class Nuevo_Accion(TemplateView):
    template_name = "caja/Nuevo Movimiento.html"

    def Valdación(self,request):
        cantidad = request.POST['Cantidad']
        cantidad =str(cantidad)
        Tipo = request.POST['Descrpción']
        caja = Variables_Generales.objects.get(variable="Caja")
        Saldo_Caja = float(caja.valor)

        if cantidad.isdigit():
          cantidad = float(cantidad)
          if cantidad<=0 :
              messages.error(request,"Error en cantidad","Error en Cantidad")
              return  False
          else:
              if (cantidad> Saldo_Caja) and (Tipo=='Ban.Retiro' or Tipo=='Viaticos'):
                  messages.error(request,"No se puede retirar esa cantidad","Saldo insuficiente")
                  return False

        N_Recibo = request.POST['Núm. Recibo']
        N_Recibo = str(N_Recibo)

        if N_Recibo.isdigit():
            return True
        else:
            return False

    def post(self,request,*args,**kwargs):
        v= self.Valdación(request)

        if v== True:
            cantidad = float(request.POST['Cantidad'])
            N_recibo = int(request.POST['Núm. Recibo'])
            caja = Variables_Generales.objects.get(variable="Caja")
            Saldo_Caja =  float(caja.valor)
            Tipo = request.POST['Descrpción']
            Temp_Caja.objects.filter(Usuario=self.request.user.username).delete()
            if Tipo=='Ban.Ingreso':
                A1 = Temp_Caja(
                    Usuario=self.request.user.username,
                    Num_Recibo=N_recibo,
                    Descripción="Ingreso desde el Banco",
                    Entrada=cantidad,
                    Salida=0.0,
                    Saldo=round(Saldo_Caja+cantidad,2)
                )
                A1.save()
                caja.valor = str(round(Saldo_Caja+cantidad))
            if Tipo=="Ban.Retiro":
                A1 = Temp_Caja(
                    Usuario=self.request.user.username,
                    Num_Recibo=N_recibo,
                    Descripción="Retiro hacia el Banco",
                    Entrada=0.0,
                    Salida=cantidad,
                    Saldo=round(Saldo_Caja - cantidad, 2)
                )
                A1.save()
                caja.valor = str(round(Saldo_Caja - cantidad))
            if Tipo=="Viaticos":
                A1 = Temp_Caja(
                    Usuario=self.request.user.username,
                    Num_Recibo=N_recibo,
                    Descripción="Viaticos",
                    Entrada=0.0,
                    Salida=cantidad,
                    Saldo=round(Saldo_Caja - cantidad, 2)
                )
                A1.save()
                caja.valor = str(round(Saldo_Caja - cantidad))

            caja.save()

            return redirect('caja:mostrar')

        else:
            return  render(request,"caja/Nuevo Movimiento.html")

class Mostrar_Caja(ListView):
    template_name = "caja/Mostrar Caja.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data()
        ctx.update({
            'Fecha': date.today()
        })

        return ctx

    def get_queryset(self):
        return Temp_Caja.objects.filter(Usuario=self.request.user.username)