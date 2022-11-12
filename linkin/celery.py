import os

import configurations
from celery import Celery

if not os.getenv("DJANGO_SETTINGS_MODULE"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "linkin.config")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Production")
    configurations.setup()

app = Celery('linkin')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
