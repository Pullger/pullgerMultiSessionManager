import os
from django.apps import AppConfig
from pullgerMultiSessionManager import core


class MultiSessionManagerCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pullgerMultiSessionManager'
    multi_session_manager = None

    def ready(self):
        self.multi_session_manager = core.ConnectionManager()
        if os.environ.get('RUN_MAIN') == 'true':
            pass
