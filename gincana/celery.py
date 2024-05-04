from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gincana.settings')

app = Celery('gincana')
app.conf.enable_utc = False

app.conf.update(timezone = 'Europe/Madrid')

app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    'terminar-gincana': {
        'task': 'tasks.tasks.terminar_gincana',
        'schedule': crontab(minute='*')
    }
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
