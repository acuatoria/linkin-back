from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'linkin.url'
    verbose_name = "App"

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from linkin.url import signals   # noqa
