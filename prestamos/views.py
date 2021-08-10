from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from datetime import datetime
from datetime import timedelta
from django.template import  Template, context, Context
from django import forms
from django.views.generic import TemplateView, RedirectView
# Create your views here.

def Prestamos(request):
    if request.method=="POST":
        if validacion_datos(request):
            ar = open("/home/marco/PycharmProjects/djangoProject/templates/transactions/Prestamos_mostrar.html")
            Te = Template(ar.read())
            ar.close()
            ctx = generar_prestamo(request)
            final = Te.render(ctx)

            return HttpResponse(final)


    return  render(request, "transactions/Prestamos.html")

def validacion_datos(request):
    id = request.POST['Identidad']
    if len(id) != 13:
        messages.error(request, "Error en Identidad", "Debe medir 13")
        return False
    FO = request.POST['Fecha Otorgado']
    FO = datetime.strptime(FO,"%Y-%m-%d").date()
    FP = request.POST['Fecha Primera Cuota']
    FP = datetime.strptime(FP,"%Y-%m-%d").date()
    delta= FP-FO
    dias = int(delta.days)
    if dias<=30:
        messages.error(request, "Error Fecha de Pago de Primera Cuota ", "Debe medir 13")
        return False
    return  True


def generar_prestamo(request):

    Tmensual= request.POST['Interes']
    Tmensual = float(Tmensual)/12
    lista_cuotas= generar_cuotas(request)
    ctx = Context({"Cliente": request.POST['Cliente'],
                   "Identidad": request.POST['Identidad'],
                   "Fecha_O": request.POST['Fecha Otorgado'],
                   "Fecha_P": request.POST['Fecha Primera Cuota'],
                   "Plazo": request.POST['Plazo'],
                   "Tanual": request.POST['Interes'],
                   "Tmensual": str(Tmensual),
                   "Pgracia": request.POST['Periodo de Gracia'],
                   "Descuento": request.POST['Descuento'],
                   "Monto": request.POST['Monto'],
                   "Mora":  "0.0001",
                   "Lista_Cuotas": lista_cuotas

                   })
    return ctx

def generar_cuotas(request):
    monto = float(request.POST['Monto'])
    Taza_anual = float(request.POST['Interes'])
    Taza_anual=Taza_anual/100
    Taza_mensual=(Taza_anual/12)
    num_cuotas = int(request.POST['Plazo'])
    Interese = monto*(Taza_anual*num_cuotas/12)
    capital_mensual= monto/num_cuotas
    interes_mensual= Interese/num_cuotas
    Total_prestamo= monto + Interese
    fecha_1 = request.POST['Fecha Primera Cuota']
    fecha_1= datetime.strptime(fecha_1,"%Y-%m-%d").date()

    plan_pago=[]
    pagado=0
    for x in range(num_cuotas):
        mes=[]
        cuota=x+1
        fecha = fecha_1 + timedelta(days=30*x)
        mes.append(fecha)
        mes.append(cuota)
        mes.append(capital_mensual)
        mes.append(interes_mensual)
        saldo = Total_prestamo-pagado
        mes.append(saldo)
        plan_pago.append(mes)
    return  plan_pago

