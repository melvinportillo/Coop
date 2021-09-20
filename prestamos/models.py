from django.db import models

# Create your models here.


class Datos_prestamos(models.Model):
    id_cliente = models.CharField(max_length=15)
    id_prestamo= models.IntegerField()
    nombre_cliente= models.CharField(max_length=50)
    miembro = models.CharField(max_length=1)
    fecha_otorgado= models.DateField()
    fecha_vencimiento= models.DateField()
    plazo_meses= models.IntegerField()
    taza_mensual= models.FloatField()
    Periodo_Gracia= models.IntegerField()
    Taza_Descuento= models.FloatField()
    Monto = models.FloatField()


class Acciones_Prestamos(models.Model):
    id_prestamo = models.IntegerField()
    num_cuota= models.IntegerField()
    Fecha_Pago= models.DateField()
    Num_recibo= models.IntegerField()
    Monto= models.FloatField()
    Capital = models.FloatField()
    Descuento = models.FloatField()
    Intereses = models.FloatField()
    Pago = models.FloatField()
    Saldo = models.FloatField()
    Saldo_mora = models.FloatField()
    Intereses_moratorios= models.FloatField()

class Temp_Datos_prestamos(models.Model):
    Usuario = models.CharField(max_length=15)
    id_persona = models.CharField(max_length=15)
    nombre_cliente = models.CharField(max_length=50)
    miembro = models.CharField(max_length=1)
    fecha_otorgado = models.DateField()
    plazo_meses = models.IntegerField()
    taza_mensual = models.FloatField()
    Intereses = models.FloatField()
    Periodo_Gracia = models.IntegerField()
    Taza_Descuento = models.FloatField()
    Monto = models.FloatField()


class Temp_Acciones_Prestamos(models.Model):
    Usuario = models.CharField(max_length=15)
    num_cuota = models.IntegerField()
    fecha_cuota = models.DateField()
    capital = models.FloatField()
    Descuento = models.FloatField()
    Intereses = models.FloatField()
    total_cuota = models.FloatField()
    saldo = models.FloatField()

class Variables_Generales(models.Model):
    variable = models.CharField(max_length=50)
    valor = models.CharField(max_length=50)
