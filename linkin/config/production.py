import os

from .common import Common


class Production(Common):
    INSTALLED_APPS = Common.INSTALLED_APPS
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
    # Site
    # https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS', '*')]
    INSTALLED_APPS += ("gunicorn", )

    INSTALLED_APPS += ('storages',)
    AWS_STORAGE_BUCKET_NAME = os.getenv('DJANGO_AWS_STORAGE_BUCKET_NAME', '')
    MEDIA_URL = f'https://s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/'

    # https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/http-caching#cache-control
    # Response can be cached by browser and any intermediary caches (i.e. it is "public") for up to 1 day
    # 86400 = (60 seconds x 60 minutes x 24 hours)
    AWS_HEADERS = {
        'Cache-Control': 'max-age=86400, s-maxage=86400, must-revalidate',
    }
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': os.getenv('REDIS_URL'),
        }
    }
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

    CSRF_TRUSTED_ORIGINS = ['https://' + x for x in os.getenv('ALLOWED_HOSTS', '').split(',')]

    ADMINS = [
        (os.getenv('ADMIN_NAME', ''), os.getenv('ADMIN_EMAIL', ''))
    ]

    # CONFIGURACION MAIL GMAIL
    # ------------------------------------------------------------------------------
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', True)
    EMAIL_HOST = os.getenv('EMAIL_HOST', '')
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
    EMAIL_PORT = os.getenv('EMAIL_PORT', 587)

    CELERY_BROKER_URL = os.getenv('REDIS_URL')
    CELERY_RESULT_BACKEND = os.getenv('REDIS_URL')
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'

    CELERY_RESULT_BACKEND = 'django-db'
    CELERY_CACHE_BACKEND = 'django-cache'

    DRF_RECAPTCHA_SECRET_KEY = os.getenv('DRF_RECAPTCHA_SECRET_KEY', '')
