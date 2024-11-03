import os


# Django basic setup
SECRET_KEY = "fake-key"
INSTALLED_APPS = [
    "gdpr_manager",
    "tests",
]

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        'NAME': os.path.join(PROJECT_DIR, 'django-gdpr-manager.db'),
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# GDPR Manager settings
"""
Tests have to be excluded or it would start registering models
and erroring etc. We don't want that.
"""
# GDPR_MANAGER_EXCLUDE_DEFAULT excludes all the necessary ones
GDPR_MANAGER_EXCLUDE = []
# Easy defaults here
GDPR_MANAGER_SEARCH_TYPES = [
    {"key": "user_id", "verbose_name": "User ID"},
    {"key": "email", "verbose_name": "Email"},
]
# Turned off or every time you import any test models it 
# will scream as some are deliberately setup wrong
GDPR_MANAGER_REQUIRE_CHECK = False
