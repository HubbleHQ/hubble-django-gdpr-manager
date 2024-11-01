from django.apps import AppConfig
from django.db.models.signals import class_prepared

from .handlers import register_gdpr_model


class GdprManagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gdpr_manager"
    verbose_name = "GDPR Manager"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_prepared.connect(register_gdpr_model)
