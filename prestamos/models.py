from django.db import models

# Create your models here.


class Datos_prestamos(models.Model):
    id_prestamo= models.IntegerField()
    nombre_cliente= models.CharField(max_length=50)
    fecha_otorgado= models.DateField()
    fecha_vencimiento= models.DateField()
    plazo_meses= models.IntegerField()
    taza_mensual= models.FloatField()
    Periodo_Gracia= models.IntegerField()
    Taza_Descuento= models.FloatField()
    Monto = models.FloatField()
    Recargos_mora= models.FloatField()

class Acciones_Prestamos(models.Model):
    num_cuota= models.IntegerField()
    Fecha_Pago= models.DateField()
    Num_recibo= models.IntegerField()
    Monto= models.FloatField()
    Capital = models.FloatField()
    Intereses = models.FloatField()
    Saldo = models.FloatField()

