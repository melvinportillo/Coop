from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView
# Create your views here.

def Prestamos(request):
    if request.method=="post":
        return render(request, "transactions/Prestamos.html")

    return  render(request, "transactions/Prestamos.html")
