# Generated by Django 4.2.11 on 2024-05-21 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0011_invitado_respondidas'),
    ]

    operations = [
        migrations.CreateModel(
            name='Puntuacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntuacion', models.IntegerField(verbose_name='puntuacion')),
                ('invitado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.invitado')),
                ('respuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.respuesta')),
            ],
        ),
    ]
