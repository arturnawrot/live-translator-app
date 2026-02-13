# tongues_api/apps.py
from django.apps import AppConfig
from django.conf import settings
import os

class TonguesApiConfig(AppConfig):
    name = 'tongues_api'
    verbose_name = 'Tongues API Client'

    def ready(self):
        settings.TONGUES_API_KEY = os.getenv('TONGUES_API_KEY')

        from . import tongues_api
