from django.db import models
from django.utils.timezone import now
# Create your models here.

class Inventario (models.Model):
    Codigo = models.CharField(max_length=15)
    Descripcion = models.CharField(max_length=50)
    Fecha_Ingreso = models.DateField(default= now())
    Valor = models.FloatField()

class Temp_Inventario(models.Model):
    Usuario = models.CharField(max_length=50)
    Codigo = models.CharField(max_length=15)
    Descripcion = models.CharField(max_length=50)
    Fecha_Ingreso = models.DateField(default=now())
    Valor = models.FloatField()