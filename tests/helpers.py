from unittest import mock

from gdpr_manager.registry import Registry

class GDPRManagerMocks:
    def setup_settings_mocks(self, values):
        # Setup setting mocks
        if "GDPR_MANAGER_SEARCH_TYPES" in values:
            settings_gdpr_search_types_patcher = mock.patch(
                "gdpr_manager.settings.GDPR_MANAGER_SEARCH_TYPES",
                values.get("GDPR_MANAGER_SEARCH_TYPES"),
            )
            self.mock_settings_gdpr_search_types = (
                settings_gdpr_search_types_patcher.start()
            )
            self.addCleanup(settings_gdpr_search_types_patcher.stop)

        if "GDPR_MANAGER_EXCLUDE"  in values:
            settings_gdpr_manager_require_exclude_patcher = mock.patch(
                "gdpr_manager.settings.GDPR_MANAGER_EXCLUDE",
                values.get("GDPR_MANAGER_EXCLUDE"),
            )

            self.mock_gdpr_manager_require_exclude = (
                settings_gdpr_manager_require_exclude_patcher.start()
            )
            self.addCleanup(settings_gdpr_manager_require_exclude_patcher.stop)

        if "GDPR_MANAGER_REQUIRE_CHECK" in values:
            settings_gdpr_manager_require_check_patcher = mock.patch(
                "gdpr_manager.settings.GDPR_MANAGER_REQUIRE_CHECK",
                values.get("GDPR_MANAGER_REQUIRE_CHECK")
            )
            self.mock_gdpr_manager_require_check = (
                settings_gdpr_manager_require_check_patcher.start()
            )
            self.addCleanup(settings_gdpr_manager_require_check_patcher.stop)

    def setup_registry_mocks(self):
        """
        The registry needs to be mocked for every test as it is a singleton
        and will explode in much unhappiness otherwise

        If there are admin tests it will also need to be mocked in here as 
        admin talks directly to the registry as well
        """
        new_registry = Registry()

        registry_mock_patcher = mock.patch(
            "gdpr_manager.handlers.gdpr_registry",
            new_registry
        )
        self.mock_registry = (
            registry_mock_patcher.start()
        )
        self.addCleanup(registry_mock_patcher.stop)

