# Generated by Django 5.0.3 on 2024-03-09 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gincana',
            name='imagen',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to='gincana/', verbose_name='Imagen de la gincana'),
        ),
        migrations.AlterField(
            model_name='gincana',
            name='descripcion',
            field=models.TextField(blank=True, verbose_name='Descirpción de la gincana'),
        ),
        migrations.AlterField(
            model_name='gincana',
            name='edicion',
            field=models.IntegerField(blank=True, null=True, verbose_name='Edición de la gincana'),
        ),
        migrations.AlterField(
            model_name='gincana',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación'),
        ),
        migrations.AlterField(
            model_name='gincana',
            name='titulo',
            field=models.CharField(max_length=100, verbose_name='Nombre de la gincana'),
        ),
        migrations.AlterField(
            model_name='gincana',
            name='visibilidad',
            field=models.BooleanField(default=False, verbose_name='Visibilidad de la gincana'),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='fecha_nacimiento',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de nacimiento'),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='telefono',
            field=models.IntegerField(blank=True, null=True, verbose_name='Teléfono'),
        ),
    ]
