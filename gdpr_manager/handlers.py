"""
Signal handlers
"""

from .registry import gdpr_registry
from .helpers import gdpr_subclass_example, gdpr_meta_example
from .models import GDPRModel
from . import settings


def check_search_types(model):
    # Throw errors if gdpr meta fields are missing, aim is to
    # explain what should be there clearly
    missing_keys = []

    for search_type in settings.GDPR_MANAGER_SEARCH_TYPES:
        search_type_key = search_type.get("key")
        if not hasattr(model.GDPRMeta, f"search_{search_type_key}_fields"):
            missing_keys.append(f"search_{search_type_key}_fields")

    if missing_keys:
        exception_message = (
            f"\033[1mMissing required properties in {model.__name__} GDPRMeta: "
            f"{','.join(missing_keys)}\033[0m \n"
            f"{gdpr_meta_example(missing_keys, model_name=model.__name__)}"
        )
        raise Exception(exception_message)


def register_gdpr_model(sender, **kwargs):
    """
    Register all models that inherit from GDPRModel and have the GDPRMeta class
    Error if a model is part way setup. Later add in a check for all models so they
    error if a model isn't setup with GDPR in mind.
    """
    # 3rd party apps we want to exclude from the model require.
    app_name = sender.__module__.split(".")[0]

    if (
        app_name in settings.GDPR_MANAGER_EXCLUDE 
        or sender.__name__ in settings.GDPR_MANAGER_EXCLUDE_MODELS
    ):
        return

    is_subclass = issubclass(sender, GDPRModel)
    has_gdpr_meta = sender.__dict__.get("GDPRMeta")

    if is_subclass and has_gdpr_meta:
        check_search_types(sender)
        gdpr_registry.register(sender)
    elif settings.GDPR_MANAGER_REQUIRE_CHECK:
        raise Exception(
            f"\033[1mModel {sender.__name__} does not have GDPR Manager setup correctly or at all\033[0m\n"
            f"module: {sender.__module__}\n"
            "Every model is required use the GDPR Manager to manage GDPR data requests\n"
            "and to understand what personal data is held.\n"
            "If there is no relevant data for a property, set it as an empty list. \n"
            "If any of the properties are excluded, you will get an error. \n"  # Not true right now need to fix that
            f"{gdpr_subclass_example(model_name=sender.__name__, with_meta_example=True)}\n"
        )
