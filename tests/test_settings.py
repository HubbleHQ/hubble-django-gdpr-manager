SECRET_KEY = "fake-key"
INSTALLED_APPS = [
    "gdpr_manager",
    "tests",
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    }
}
