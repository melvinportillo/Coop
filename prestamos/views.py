from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView
# Create your views here.

class Paso(TemplateView):
    template_name='transactions/Prestamos.html'