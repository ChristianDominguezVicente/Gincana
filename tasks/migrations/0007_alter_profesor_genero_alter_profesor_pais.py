# Generated by Django 5.0.3 on 2024-03-19 15:54

import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_alter_gincana_activa_alter_profesor_genero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profesor',
            name='genero',
            field=models.CharField(choices=[('H', 'Hombre'), ('M', 'Mujer'), ('O', 'Otro')], default='M', max_length=1, null=True, verbose_name='Género'),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='pais',
            field=django_countries.fields.CountryField(max_length=2, null=True),
        ),
    ]
