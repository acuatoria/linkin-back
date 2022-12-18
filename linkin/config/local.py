import os
from .common import Common
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Local(Common):
    DEBUG = True

    # Testing
    INSTALLED_APPS = Common.INSTALLED_APPS
    INSTALLED_APPS += ('django_nose',)
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    NOSE_ARGS = [
        BASE_DIR,
        '-s',
        '--nologcapture',
        '--with-coverage',
        '--cover-package=linkin',
        '--cover-html'
    ]

    # Mail
    # EMAIL_HOST = 'localhost'
    # EMAIL_PORT = 1025
    # EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    SHELL_PLUS_IMPORTS = [
        'from linkin.comments.models import Comment',
    ]

    CELERY_TASK_ALWAYS_EAGER = True

    DRF_RECAPTCHA_SECRET_KEY = os.getenv('DRF_RECAPTCHA_SECRET_KEY', '')
    DRF_RECAPTCHA_TESTING = True
