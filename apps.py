import os

from django.apps import AppConfig
from django.conf import settings

from pullgerMultiSessionManager import core


class MultiSessionManagerCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pullgerMultiSessionManager'
    multi_session_manager = None

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true' or settings.TESTING is True:
            self.multi_session_manager = core.ConnectionManager()
