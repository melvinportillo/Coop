from django.shortcuts import render
from django.contrib import messages
from django import forms
from django.views.generic import TemplateView, RedirectView
# Create your views here.

def Prestamos(request):
    if request.method=="POST":
        id = request.POST['Identidad']
        if len(id)!=13:
            messages.error(request,"Error en Identidad","Debe medir 14")
        #return render(request, "transactions/Prestamos.html")



    return  render(request, "transactions/Prestamos.html")
