# Generated by Django 3.2.6 on 2021-10-13 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temp_acciones_prestamos',
            name='Usuario',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='temp_datos_prestamos',
            name='Usuario',
            field=models.CharField(max_length=50),
        ),
    ]
