from celery import shared_task
from .models import Gincana, GincanaJugada, Invitado, Puntuacion
import datetime 
from datetime import datetime, timezone, time
from pytz import timezone as t
from django.shortcuts import get_object_or_404

@shared_task(bind=True)
def terminar_gincana(self):
    gincanas = {'activas': [], 'desactivadas': []}
    gincanas_activas = Gincana.objects.filter(activa=True)
    for gincana in gincanas_activas:
        if gincana.duracion <= datetime.now(t('Europe/Madrid')).time():
            gincana.activa = False
            gincana.save()

            invitados = Invitado.objects.filter(gincana_id=gincana.id)
            for invitado in invitados:
                puntos = Puntuacion.objects.filter(invitado_id=invitado.usuario)
                puntuacion = 0
                for punto in puntos:
                    puntuacion+=punto.respuesta.puntos

                duracion = datetime.now(timezone.utc) - gincana.edicion

                total = int(duracion.total_seconds())
                horas, resto = divmod(total, 3600)
                minutos, segundos = divmod(resto, 60)

                duracion = time(horas, minutos, segundos)
                
                if GincanaJugada.objects.filter(gincana=gincana, invitado=invitado).exists():
                    gincanaJugada = get_object_or_404(GincanaJugada, invitado=invitado)
                    if gincanaJugada.duracion == time(0, 0, 0):
                        gincanaJugada.duracion = duracion
                        gincanaJugada.save()
                else:
                    gincanaJugada = GincanaJugada.objects.create(
                        duracion=duracion,
                        total_puntos=puntuacion,
                        edicion=gincana.edicion,
                        gincana_id=gincana.id,
                        invitado_id=invitado.usuario
                    )
                    gincanaJugada.save()
            gincanas['desactivadas'].append((gincana.titulo, gincana.duracion))
        else:
            gincanas['activas'].append((gincana.titulo, gincana.duracion))
    return gincanas