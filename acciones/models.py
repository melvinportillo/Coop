from django.db import models

# Create your models here.
class Datos_Accionista(models.Model):
    Nombre= models.CharField(max_length=50)
    Identidad = models.CharField(max_length=15)
    Fecha_Ingreso = models.DateField()
    Fundador = models.CharField(max_length=1)

class Temp_Datos_Accionista(models.Model):
    Usuario = models.CharField(max_length=50)
    Nombre = models.CharField(max_length=50)
    Identidad = models.CharField(max_length=15)
    Fecha_Ingreso = models.DateField()
    Fundador = models.CharField(max_length=1)

class Acciones_accionista(models.Model):
    Fecha = models.DateField()
    Identidad = models.CharField(max_length=15)
    Num_Recibo= models.IntegerField()
    Reglamento = models.FloatField()
    Extaordinaria = models.FloatField()
    Utilidad = models.FloatField()
    Donación = models.FloatField()
    Intereses = models.FloatField()
    Perdidas = models.FloatField()
    Total = models.FloatField()

class Temp_Acciones_accionista(models.Model):
    Usuario = models.CharField(max_length=50)
    Identidad = models.CharField(max_length=15)
    Fecha = models.DateField()
    Num_Recibo = models.IntegerField()
    Reglamento = models.FloatField()
    Extaordinaria = models.FloatField()
    Utilidad = models.FloatField()
    Donación = models.FloatField()
    Intereses = models.FloatField()
    Perdidas = models.FloatField()
    Total = models.FloatField()