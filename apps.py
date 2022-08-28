import os
from django.apps import AppConfig
from pullgerMultisessionManager_1 import core


class MultisessionManagerCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pullgerMultisessionManager'
    multisessionManager = None

    def ready(self):
        self.multisessionManager = core.ConnectionManager()
        if os.environ.get('RUN_MAIN') == 'true':
            pass
