from django.db import models

# Create your models here.

class Datos_Ahorros(models.Model):
    Identidad = models.CharField(max_length=15)
    Nombre =  models.CharField(max_length=50)
    Beneficiarios= models.CharField(max_length=100)
    Observacions = models.CharField(max_length=100)

class Acciones_Ahorros(models.Model):
    Identidad = models.CharField(max_length=15)
    Fecha = models.DateField()
    Num_Recibo = models.IntegerField()
    Deposito= models.FloatField()
    Intereses = models.FloatField()
    Retiro = models.FloatField()
    Saldo = models.FloatField()

class Temp_Datos_Ahorrante(models.Model):
    usuario = models.CharField(max_length=30)
    Identidad = models.CharField(max_length=15)
    Nombre = models.CharField(max_length=50)
    Beneficiarios = models.CharField(max_length=100)
    Observacions = models.CharField(max_length=100)

class Temp_Datos_Acciones_Ahorro(models.Model):
    Identidad = models.CharField(max_length=15)
    usuario = models.CharField(max_length=30)
    Fecha = models.DateField()
    Num_Recibo = models.IntegerField()
    Deposito = models.FloatField()
    Intereses = models.FloatField()
    Retiro = models.FloatField()
    Saldo = models.FloatField()
