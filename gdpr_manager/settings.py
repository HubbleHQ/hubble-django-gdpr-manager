from django.conf import settings

GDPR_MANAGER_EXCLUDE_DEFAULT = [
    "django",
    "__fake__",
    "rest_framework",
    "gdpr_manager",
    "django_rq",
]

GDPR_MANAGER_SEARCH_TYPES = getattr(
    settings,
    "GDPR_MANAGER_SEARCH_TYPES",
    [
        {
            "key": "user_id", 
            "verbose_name": "User ID",
            "default_lookup": "exact"
        },
        {
            "key": "email",
            "verbose_name": "Email",
            "default_lookup": "iexact"
        },
    ],
)

GDPR_MANAGER_EXCLUDE = GDPR_MANAGER_EXCLUDE_DEFAULT + (
    getattr(
        settings,
        "GDPR_MANAGER_EXCLUDE",
        []
    )
)

GDPR_MANAGER_EXCLUDE_MODELS = getattr(
    settings,
    "GDPR_MANAGER_EXCLUDE_MODELS",
    []
)

GDPR_MANAGER_REQUIRE_CHECK = getattr(
    settings,
    "GDPR_MANAGER_REQUIRE_CHECK",
    True,
)
