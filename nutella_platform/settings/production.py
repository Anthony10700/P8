from . import *

SECRET_KEY = '~aO;| F;rE[??/w^zcumh(9'
DEBUG = False
ALLOWED_HOSTS = ['174.138.54.208']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # on utilise l'adaptateur postgresql
        'NAME': 'nutella_platform',
        # le nom de notre base de données créée précédemment
        'USER': 'anthony',
        # attention : remplacez par votre nom d'utilisateur !!
        'PASSWORD': 'azerty',
        'HOST': '',
        'PORT': '5432',
    }
    

    }

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://73bb3723ee034b73b4c0c6770157bd8c@o514569.ingest.sentry.io/5617931",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)


