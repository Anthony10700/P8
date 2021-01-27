from . import *

SECRET_KEY = '-~aO;| F;rE[??/w^zcumh(9'
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
        'HOST': '127.0.0.1',
        'PORT': '5432',
        }










