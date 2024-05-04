from celery import shared_task
from .models import Gincana
from datetime import datetime
from pytz import timezone

@shared_task(bind=True)
def terminar_gincana(self):
    gincanas = {'activas': [], 'desactivadas': []}
    gincanas_activas = Gincana.objects.filter(activa=True)
    for gincana in gincanas_activas:
        if gincana.duracion < datetime.now(timezone('Europe/Madrid')).time():
            gincana.activa = False
            gincana.save()
            gincanas['desactivadas'].append((gincana.titulo, gincana.duracion))
        else:
            gincanas['activas'].append((gincana.titulo, gincana.duracion))
    return gincanas