from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from datetime import timedelta
from django.template import  Template, Context
from django import forms
from django.views import View

from prestamos.models import Temp_Datos_prestamos, Temp_Acciones_Prestamos
from django.views.generic import TemplateView, RedirectView, ListView
# Create your views here.
from prestamos.utils import render_to_pdf

def Prestamos(request):
    if request.method=="POST":
        if validacion_datos(request):
            Temp_Datos_prestamos.objects.all().delete()
            Temp_Acciones_Prestamos.objects.all().delete()
            generar_prestamo(request)
            return  redirect("mostrar/")


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

    Tanual= float(request.POST['Interes'])/100
    Tmensual = float(Tanual)/12
    monto = float(request.POST['Monto'])
    num_cuotas = int(request.POST['Plazo'])
    Interese = monto * (Tanual * num_cuotas / 12)

    temp = Temp_Datos_prestamos(
        id_persona=request.POST['Identidad'],
        nombre_cliente=request.POST['Cliente'],
        fecha_otorgado=datetime.strptime(request.POST['Fecha Otorgado'],"%Y-%m-%d").date(),
        plazo_meses= int(request.POST['Plazo']),
        taza_mensual= Tmensual,
        Periodo_Gracia= int(request.POST['Periodo de Gracia']),
        Taza_Descuento= float(request.POST['Descuento']),
        Intereses=Interese,
        Monto= float(request.POST['Monto']),


    )
    temp.save()
    generar_cuotas(request)


def generar_cuotas(request):
    monto = float(request.POST['Monto'])
    Taza_anual = float(request.POST['Interes'])
    Taza_anual=Taza_anual/100
    Taza_mensual=(Taza_anual/12)
    num_cuotas = int(request.POST['Plazo'])
    Interese = monto*(Taza_anual*num_cuotas/12)
    capital_mensual= round(monto/num_cuotas,2)
    interes_mensual= round(Interese/num_cuotas,2)
    Total_prestamo= monto + Interese
    fecha_1 = request.POST['Fecha Primera Cuota']
    fecha_1= datetime.strptime(fecha_1,"%Y-%m-%d").date()

    plan_pago=[]
    pagado=0
    for x in range(num_cuotas):
        temp =Temp_Acciones_Prestamos(
            num_cuota=x+1,
            fecha_cuota=fecha_1 + timedelta(days=30*x),
            capital= capital_mensual,
            Intereses= interes_mensual,
            total_cuota= capital_mensual+interes_mensual,
            saldo= round(Total_prestamo-pagado,2),
        )
        pagado = pagado+ capital_mensual+interes_mensual
        temp.save()


class mostra_prestamp(ListView):
    template_name = 'transactions/Prestamos_mostrar.html'
    model = Temp_Acciones_Prestamos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        info= Temp_Datos_prestamos.objects.all()
        prest= info[0]
        context.update({
            'Cliente': prest.nombre_cliente,
            'Identidad': prest.id_persona,
            'Fecha_O': prest.fecha_otorgado,
            'Plazo': prest.plazo_meses,
            'Tanual': prest.taza_mensual*12,
            'Tmensual': prest.taza_mensual,
            'Pgracia': prest.Periodo_Gracia,
            'Descuento': prest.Taza_Descuento,
            'Monto':prest.Monto,
            'Intereses': prest.Intereses,

            'Mora': "0.0001"

        })
        return  context

    def get_queryset(self):
        return Temp_Acciones_Prestamos.objects.all()


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        info = Temp_Datos_prestamos.objects.all()
        prest = info[0]
        lista= Temp_Acciones_Prestamos.objects.all()
        context={
            'Cliente': prest.nombre_cliente,
            'Identidad': prest.id_persona,
            'Fecha_O': prest.fecha_otorgado,
            'Plazo': prest.plazo_meses,
            'Tanual': prest.taza_mensual * 12,
            'Tmensual': prest.taza_mensual,
            'Pgracia': prest.Periodo_Gracia,
            'Descuento': prest.Taza_Descuento,
            'Monto': prest.Monto,
            'Intereses': prest.Intereses,
            'object_list': lista,
            'Mora': "0.0001"

        }
        pdf = render_to_pdf('pdf/prestamo_pdf.html', context)
        return HttpResponse(pdf, content_type='prestamos/pdf')