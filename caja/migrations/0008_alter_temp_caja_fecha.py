# Generated by Django 3.2.6 on 2021-09-19 02:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('caja', '0007_alter_temp_caja_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temp_caja',
            name='Fecha',
            field=models.DateField(default=datetime.datetime(2021, 9, 19, 2, 27, 45, 652835, tzinfo=utc)),
        ),
    ]
