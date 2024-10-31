from unittest import mock

from django.test import TestCase

from gdpr_manager.handlers import check_search_types

from ..helpers import GDPRManagerMocks
from ..test_app.models import (
    ModelWithGDPRMeta
)


class TestModelsCheckSearchTypes(TestCase, GDPRManagerMocks):
    def setUp(self):
        self.setup_settings_mocks({
            "GDPR_MANAGER_SEARCH_TYPES": [
                {"key": "user_id", "verbose_name": "User ID"},
                {"key": "email", "verbose_name": "Email"},
            ]
        })
        self.setup_registry_mocks()
    
    def test_errors_if_missing_search_type_field(self):
        with mock.patch(
            "gdpr_manager.settings.GDPR_MANAGER_SEARCH_TYPES",
            [
                {"key": "user_id", "verbose_name": "User ID"},
                {"key": "email", "verbose_name": "Email"},
                {"key": "extra-search-type", "verbose_name": "Extra Search Type"},
            ],
        ):
            with self.assertRaises(Exception) as context:
                check_search_types(ModelWithGDPRMeta)
                
            self.assertTrue(
                "Missing required properties in ModelWithGDPRMeta GDPRMeta: "
                "search_extra-search-type_fields" in str(context.exception)
            )

    def test_does_not_error_if_all_search_type_fields_are_present(self):
        try:
            check_search_types(ModelWithGDPRMeta)
        except Exception:
            self.fail("Should not fail if all search type information was added.")
