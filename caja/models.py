from django.db import models
from datetime import date
# Create your models here.
class Caja(models.Model):
    Fecha = models.DateField()
    Num_Recibo = models.IntegerField()
    Descripción = models.CharField(max_length=50)
    Entrada = models.FloatField()
    Salida = models.FloatField()
    Saldo = models.FloatField()

class Temp_Caja(models.Model):
    Usuario = models.CharField(max_length=15)
    Fecha = models.DateField(default=date.today())
    Num_Recibo = models.IntegerField()
    Descripción = models.CharField(max_length=50)
    Entrada = models.FloatField()
    Salida = models.FloatField()
    Saldo = models.FloatField()