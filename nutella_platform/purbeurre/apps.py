from django.apps import AppConfig
import os

class PurbeurreConfig(AppConfig):
    if os.environ.get('ENV') == 'PRODUCTION':
        name = 'nutella_platform.purbeurre'
    else:
        name = 'purbeurre'
