# Generated by Django 3.2.6 on 2021-09-19 02:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0004_auto_20210919_0210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventario',
            name='Fecha_Ingreso',
            field=models.DateField(default=datetime.datetime(2021, 9, 19, 2, 27, 45, 653482, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='temp_inventario',
            name='Fecha_Ingreso',
            field=models.DateField(default=datetime.datetime(2021, 9, 19, 2, 27, 45, 653861, tzinfo=utc)),
        ),
    ]
