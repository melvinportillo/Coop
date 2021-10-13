from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib import  messages
from .models import Temp_Caja, Caja
from datetime import  date, timedelta
from core.models import Libro_Diario, Libro_Mayor
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
            #caja = Variables_Generales.objects.get(variable="Caja")
            caja=0.0
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

            Movimiento = Temp_Caja.objects.get(Usuario=self.request.user.username)

            A1 = Caja(
                Fecha=Movimiento.Fecha,
                Num_Recibo=Movimiento.Num_Recibo,
                Entrada=Movimiento.Entrada,
                Descripción=Movimiento.Descripción,
                Salida=Movimiento.Salida,
                Saldo=Movimiento.Saldo
            )
            A1.save()
#Libros
            if Movimiento.Descripción=="Ingreso desde el Banco":
                M1 = Libro_Diario(
                    Usuario=self.request.user,
                    Fecha=date.today(),
                    Descripcion=Movimiento.Descripción,
                    Debe="Caja: + " + str(Movimiento.Entrada),
                    Haber="Banco: -" + str(Movimiento.Entrada),
                    Cuadre=0.0
                )
                M1.save()
                c1 = Libro_Mayor.objects.filter(Cuenta="Banco").count()
                banco_saldo=0
                if c1>0:
                    banco_saldo=Libro_Mayor.objects.filter(Cuenta="Banco").last().Cuadre
                M2 = Libro_Mayor(
                    Cuenta="Banco",
                    Debe=0.0,
                    Haber= Movimiento.Entrada,
                    Fecha=date.today(),
                    Cuadre=banco_saldo-Movimiento.Entrada,
                    Descripcion=Movimiento.Descripción
                )
                M2.save()
                caja_saldo=0
                c2 = Libro_Mayor.objects.filter(Cuenta="Caja").count()
                if c2>0:
                    caja_saldo= Libro_Mayor.objects.filter(Cuenta="Caja").last().Cuadre
                M3 = Libro_Mayor(
                    Cuenta="Caja",
                    Debe=Movimiento.Entrada,
                    Haber=0.0,
                    Fecha=date.today(),
                    Cuadre=caja_saldo+Movimiento.Entrada,
                    Descripcion=Movimiento.Descripción,
                )
                M3.save()

            if Movimiento.Descripción=="Retiro hacia el Banco":
                M1 = Libro_Diario(
                    Usuario=self.request.user,
                    Fecha=date.today(),
                    Descripcion=Movimiento.Descripción,
                    Debe="Banco: +" + str(Movimiento.Salida),
                    Haber="Caja: - " + str(Movimiento.Salida),
                    Cuadre=0.0
                )
                M1.save()
                c1 = Libro_Mayor.objects.filter(Cuenta="Banco").count()
                banco_saldo=0
                if c1>0:
                    banco_saldo=Libro_Mayor.objects.filter(Cuenta="Banco").last().Cuadre
                M2 = Libro_Mayor(
                    Cuenta="Banco",
                    Debe=Movimiento.Salida,
                    Haber= 0.0,
                    Fecha=date.today(),
                    Cuadre=banco_saldo+Movimiento.Salida,
                    Descripcion=Movimiento.Descripción
                )
                M2.save()
                caja_saldo=0
                c2 = Libro_Mayor.objects.filter(Cuenta="Caja").count()
                if c2>0:
                    caja_saldo= Libro_Mayor.objects.filter(Cuenta="Caja").last().Cuadre
                M3 = Libro_Mayor(
                    Cuenta="Caja",
                    Debe=0.0,
                    Haber=Movimiento.Salida,
                    Fecha=date.today(),
                    Cuadre=caja_saldo-Movimiento.Salida,
                    Descripcion=Movimiento.Descripción,
                )
                M3.save()

            if Movimiento.Descripción=="Viaticos":
                M1 = Libro_Diario(
                    Usuario=self.request.user,
                    Fecha=date.today(),
                    Descripcion=Movimiento.Descripción,
                    Debe="Viaticos: +" + str(Movimiento.Salida),
                    Haber="Caja: - " + str(Movimiento.Salida),
                    Cuadre=0.0
                )
                M1.save()
                c1 = Libro_Mayor.objects.filter(Cuenta="Viaticos").count()
                banco_saldo=0
                if c1>0:
                    banco_saldo=Libro_Mayor.objects.filter(Cuenta="Viaticos").last().Cuadre
                M2 = Libro_Mayor(
                    Cuenta="Viaticos",
                    Debe=Movimiento.Salida,
                    Haber= 0.0,
                    Fecha=date.today(),
                    Cuadre=banco_saldo-Movimiento.Salida,
                    Descripcion=Movimiento.Descripción
                )
                M2.save()
                caja_saldo=0
                c2 = Libro_Mayor.objects.filter(Cuenta="Caja").count()
                if c2>0:
                    caja_saldo= Libro_Mayor.objects.filter(Cuenta="Caja").last().Cuadre
                M3 = Libro_Mayor(
                    Cuenta="Caja",
                    Debe=0.0,
                    Haber=Movimiento.Salida,
                    Fecha=date.today(),
                    Cuadre=caja_saldo-Movimiento.Salida,
                    Descripcion=Movimiento.Descripción,
                )
                M3.save()
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
        return Temp_Caja.objects.filter(Usuario=self.request.user.username, Fecha=date.today())


class Filtrar_Caja (TemplateView):
    template_name = "caja/Mostrar_Caja_Filtrada.html"

    def Valiadcion(self,request):
        Fecha_i = request.POST['Fecha_1']
        Fecha_f = request.POST['Fecha_2']
        if Fecha_i> Fecha_f :
            messages.error(request,"Error en fechas introducidas","Error Fechas")
            return False
        return True

    def post(self,request, *args, **kwargs):
        v= self.Valiadcion(request)
        if v==False:
            return render(request,"caja/Mostrar_Caja_Filtrada.html")
        else:
            Fecha_i = request.POST['Fecha_1']
            Fecha_f = request.POST['Fecha_2']
            ob = Caja.objects.filter(Fecha__gte=Fecha_i, Fecha__lte=Fecha_f)
            ctx = {
                'object_list':ob
            }
            return  render(request,"caja/Mostrar_Caja_Filtrada.html",ctx)
