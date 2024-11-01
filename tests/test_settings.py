# Django basic setup
SECRET_KEY = "fake-key"
INSTALLED_APPS = [
    "django_gdpr_manager",
    "tests",
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# GDPR Manager settings
"""
Tests have to be excluded or it would start registering models
and erroring etc. We don't want that.
"""
GDPR_MANAGER_EXCLUDE = [
    "tests"
]
GDPR_MANAGER_SEARCH_TYPES = [
    {"key": "user_id", "verbose_name": "User ID"},
    {"key": "email", "verbose_name": "Email"},
]
GDPR_MANAGER_REQUIRE_CHECK = True
