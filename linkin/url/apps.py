from django.apps import AppConfig
from django.core.signals import request_finished

class MyAppConfig(AppConfig):
    name = 'linkin.url'
    verbose_name = ""

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from . import signals
