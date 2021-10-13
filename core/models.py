from django.db import models

# Create your models here.
class Libro_Diario(models.Model):
    Usuario = models.CharField(max_length=50)
    Fecha = models.DateField()
    Descripcion = models.CharField(max_length=100)
    Debe = models.CharField(max_length=150)
    Haber = models.CharField(max_length=150)
    Cuadre = models.FloatField()

class Libro_Mayor(models.Model):
    Cuenta = models.CharField(max_length=50)
    Debe = models.FloatField()
    Haber = models.FloatField()
    Fecha = models.DateField()
    Cuadre = models.FloatField()
    Descripcion = models.CharField(max_length=100)

class Balance_General(models.Model):
    Cuenta = models.CharField(max_length=50)
    Saldo = models.FloatField()
    Activo = models.FloatField()
    Pasivo  = models.FloatField()
    Total = models.FloatField()

class Estado_Resultado(models.Model):
    Cuenta = models.CharField(max_length=50)
    Fecha_1= models.FloatField()
    Fecha_2 = models.FloatField()
    Saldo = models.FloatField()
    Rojo = models.FloatField()
    Amarillo = models.FloatField()
    Verde = models.FloatField()