from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from datetime import timedelta
from django.template import Template, Context, RequestContext
from django import forms
from django.views import View

from prestamos.models import Temp_Datos_prestamos, Temp_Acciones_Prestamos, Datos_prestamos, Acciones_Prestamos, Variables_Generales
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

class Inicio(TemplateView):
    template_name='transactions/Index.html'

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
    if dias<30:
        messages.error(request, "Error Fecha de Pago de Primera Cuota ", "Debe medir 13")
        return False
    return  True


def generar_prestamo(request):

    Tanual= float(request.POST['Interes'])/100
    Tmensual = float(Tanual)/12
    monto = float(request.POST['Monto'])
    num_cuotas = int(request.POST['Plazo'])
    Interese = generar_cuotas(request)

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



def generar_cuotas(request):
    monto = float(request.POST['Monto'])
    Taza_anual = float(request.POST['Interes'])
    Taza_anual=Taza_anual/100
    Taza_mensual=(Taza_anual/12)
    num_cuotas = int(request.POST['Plazo'])
    pe_gracia = int(request.POST['Periodo de Gracia'])
    cuotas_validas= num_cuotas-pe_gracia
    capital_mensual= round(monto/cuotas_validas,2)
    fecha_1 = request.POST['Fecha Primera Cuota']
    fecha_1= datetime.strptime(fecha_1,"%Y-%m-%d").date()
    saldo = monto
    descuento = float(request.POST['Descuento'])
    interes_total=0
    for x in range(num_cuotas):
        interes = round(saldo*Taza_mensual,2)
        capital_cuota= capital_mensual
        if x+1<= pe_gracia:
            capital_cuota=0
        fecha_cuota = fecha_1+ timedelta(days=30*x)
        saldo = round(saldo - capital_cuota, 2)
        cuota = Temp_Acciones_Prestamos(
            num_cuota=x+1,
            fecha_cuota=fecha_cuota,
            Descuento=0,
            capital= capital_cuota,
            Intereses= interes,
            total_cuota= round(capital_cuota+interes,2),
            saldo=saldo

        )

        interes_total=interes_total+interes
        cuota.save()
    num_c = num_cuotas
    while descuento >0:
        cuota = Temp_Acciones_Prestamos.objects.get(num_cuota=num_c)
        capital_cuota= cuota.capital
        interes = cuota.Intereses
        saldo = cuota.saldo
        total_cuota=0
        delta = capital_cuota-descuento
        new_capital=0
        des_aplicado=0
        if delta<0:
            descuento=descuento-capital_cuota
            des_aplicado=capital_cuota
        else:
            new_capital=delta
            des_aplicado=capital_cuota-delta
            new_saldo=saldo-delta
            descuento=0

        total_cuota = new_capital + interes
        #cuota.capital=round(new_capital,2)
        cuota.total_cuota=round(total_cuota,2)
        cuota.Descuento=round(des_aplicado,2)
        cuota.save()
        num_c=num_c-1

    return  interes_total



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

def Guardar(request):

    num_prestamos = Datos_prestamos.objects.all().count()
    id_presta = num_prestamos+1
    info = Temp_Datos_prestamos.objects.all()
    prest = info[0]
    coutas = Temp_Acciones_Prestamos.objects.all()
    num_cuota = int(prest.plazo_meses)
    desc= Temp_Acciones_Prestamos.Descuento
    fecha_final = coutas[num_cuota-1].fecha_cuota
    P1 =Datos_prestamos(
        id_prestamo=id_presta,
        id_cliente= prest.id_persona,
        nombre_cliente = prest.nombre_cliente,
        fecha_otorgado = prest.fecha_otorgado,
        fecha_vencimiento = fecha_final,
        plazo_meses  = prest.plazo_meses,
        taza_mensual = prest.taza_mensual,
        Periodo_Gracia = prest.Periodo_Gracia,
        Taza_Descuento = prest.Taza_Descuento,
        Monto= prest.Monto

    )
    P1.save()

    for cuota in coutas:
        P2 = Acciones_Prestamos(
            id_prestamo= id_presta,
            num_cuota= cuota.num_cuota,
            Num_recibo=0,
            Fecha_Pago= cuota.fecha_cuota,
            Monto= cuota.total_cuota,
            Capital= cuota.capital,
            Descuento=cuota.Descuento,
            Intereses= cuota.Intereses,
            Pago= 0,
            Saldo= cuota.saldo
        )
        P2.save()

    return render(request, "transactions/Libro_Diario.html")

def Buscar_Prestamo(request):
    if request.method=="POST":

            identidad = request.POST['Identidad']
            va = Variables_Generales.objects.filter(variable="Identidad_1")
            if len(va) ==0:
                n_v=Variables_Generales(
                        variable="Identidad_1",
                        valor= identidad
                )
                n_v.save()
            else:
                n_v = va[0]
                n_v.valor = identidad
                n_v.save()


            return  redirect("persona/")


    return  render(request, "transactions/Buscar_Prestamos.html")

class ListaPrestamos(ListView):
    template_name = 'transactions/Mostrar Prestamos.html'
    model = Datos_prestamos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_b = Variables_Generales.objects.get(variable="Identidad_1")
        value_id = id_b.valor
        list_prestamos= Datos_prestamos.objects.filter(id_cliente=value_id)
        cliente= ""
        id =""
        if len(list_prestamos)==0:
                cliente = "No se encontró cliente"
                id = "No se encontró cliente"
        else:
                prestamo_0= list_prestamos[0]
                cliente = prestamo_0.nombre_cliente
                id =prestamo_0.id_cliente
        context.update({
            'Cliente': cliente,
            'Identidad': id,
        })
        return context

    def get_queryset(self):
        id_b = Variables_Generales.objects.get(variable="Identidad_1")
        value_id = id_b.valor
        return Datos_prestamos.objects.filter(id_cliente=value_id)

    def post(self, request, *args, **kwargs):
        identidad = request.POST['Id_Prestamo']
        va = Variables_Generales.objects.filter(variable="Id_Prestamo_1")
        if len(va) == 0:
            n_v = Variables_Generales(
                variable="Id_Prestamo_1",
                valor=identidad
            )
            n_v.save()
        else:
            n_v = va[0]
            n_v.valor = identidad
            n_v.save()
        return  redirect("prestamo/")


class Prestamo_A_Pagar(ListView):
    template_name = "transactions/Mostra A Pagar.html"
    model = Acciones_Prestamos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_prestamo = Variables_Generales.objects.get(variable="Id_Prestamo_1")
        id_p= int(id_prestamo.valor)
        datos_prestamo= Datos_prestamos.objects.get(id_prestamo=id_p)
        context.update({
            'Cliente': datos_prestamo.nombre_cliente,
            'Identidad': datos_prestamo.id_cliente,
            'Fecha_O': datos_prestamo.fecha_otorgado,
            'Plazo': datos_prestamo.plazo_meses,
            'Tanual': datos_prestamo.taza_mensual*12,
            'Tmensual': datos_prestamo.taza_mensual,
            'Pgracia':  datos_prestamo.Periodo_Gracia,
            'Descuento': datos_prestamo.Taza_Descuento,
            'Monto': datos_prestamo.Monto,
            'Mora': "0.0001",
            'Id_Prestamo': id_p


        })
        return context

    def get_queryset(self):
        id_prestamo = Variables_Generales.objects.get(variable="Id_Prestamo_1")
        id_p = int(id_prestamo.valor)
        return Acciones_Prestamos.objects.filter(id_prestamo=id_p)

    def post(self, request, *args, **kwargs):
        id_prestamo = Variables_Generales.objects.get(variable="Id_Prestamo_1")
        id_p = int(id_prestamo.valor)
        cuota = int(request.POST['Num_Cuota'])
        cuoata_apagar= Acciones_Prestamos.objects.get(id_prestamo=id_p, num_cuota=cuota)
        cuoata_apagar.Pago= float(request.POST['Monto'])
        cuoata_apagar.Num_recibo = int(request.POST['Recibo'])
        cuoata_apagar.save()
        id_prestamo = Variables_Generales.objects.get(variable="Id_Prestamo_1")
        id_p = int(id_prestamo.valor)
        datos_prestamo = Datos_prestamos.objects.get(id_prestamo=id_p)
        ob = Acciones_Prestamos.objects.filter(id_prestamo=id_p)
        context = {
            'Cliente': datos_prestamo.nombre_cliente,
            'Identidad': datos_prestamo.id_cliente,
            'Fecha_O': datos_prestamo.fecha_otorgado,
            'Plazo': datos_prestamo.plazo_meses,
            'Tanual': datos_prestamo.taza_mensual * 12,
            'Tmensual': datos_prestamo.taza_mensual,
            'Pgracia': datos_prestamo.Periodo_Gracia,
            'Descuento': datos_prestamo.Taza_Descuento,
            'Monto': datos_prestamo.Monto,
            'Mora': "0.0001",
            'Id_Prestamo': id_p,
            'object_list': ob

        }



        return  render(request,"transactions/Mostra A Pagar.html",context)

class GeneratePdf1(View):
    def get(self, request, *args, **kwargs):
        id_prestamo= Variables_Generales.objects.get(variable="Id_Prestamo_1")
        id_p = int(id_prestamo.valor)
        datos_prestamo = Datos_prestamos.objects.get(id_prestamo=id_p)
        lista = Acciones_Prestamos.objects.filter(id_prestamo=id_p)
        context={
            'Cliente': datos_prestamo.nombre_cliente,
            'Identidad': datos_prestamo.id_cliente,
            'Fecha_O': datos_prestamo.fecha_otorgado,
            'Plazo': datos_prestamo.plazo_meses,
            'Tanual': datos_prestamo.taza_mensual * 12,
            'Tmensual': datos_prestamo.taza_mensual,
            'Pgracia': datos_prestamo.Periodo_Gracia,
            'Descuento': datos_prestamo.Taza_Descuento,
            'Monto': datos_prestamo.Monto,
            'object_list': lista,
            'Mora': "0.0001"

        }
        pdf = render_to_pdf('pdf/prestamo_con_pagos.html', context)
        return HttpResponse(pdf, content_type='prestamos/pdf')