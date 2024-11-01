from django.test import TestCase

from gdpr_manager.handlers import register_gdpr_model

from ..helpers import GDPRManagerMocks
from ..test_app.models import (
    ModelWithGDPRMeta,
    ModelWithoutGDPRMeta,
    ModelWithoutGDPRSubclass,
    ModelWithoutGDPRSubclassOrMeta
)


class TestRegister(TestCase, GDPRManagerMocks):
    def setUp(self):
        self.setup_settings_mocks({
            "GDPR_MANAGER_EXCLUDE": [],
            "GDPR_MANAGER_REQUIRE_CHECK": True
        })
        self.setup_registry_mocks()

    def test_should_register_model_if_has_gdpr_subclass_and_meta(self):
        """
        Should add the model to the gdpr_registry if it has the GDPRModel
        subclass and GDPRMeta
        """
        register_gdpr_model(ModelWithGDPRMeta)
        self.assertIn(str(ModelWithGDPRMeta._meta), self.mock_registry.models)

    def test_should_not_register_model_if_model_has_no_gdpr_meta(self):
        """
        Should not register if the model does not have GDPRMeta
        """
        with self.assertRaises(Exception):
            register_gdpr_model(ModelWithoutGDPRMeta)
            self.assertNotIn(str(ModelWithoutGDPRMeta._meta), self.mock_registry.models)

    def test_should_not_register_model_if_model_has_no_gdpr_subclass(self):
        """
        Should not register if model does not have the GDPRModel subclass
        """
        with self.assertRaises(Exception):
            register_gdpr_model(ModelWithoutGDPRSubclass)
            self.assertNotIn(str(ModelWithoutGDPRSubclass._meta), self.mock_registry.models)


    def test_should_not_register_model_if_model_has_no_gdpr_subclass_or_meta(self):
        """
        Should not register if model does not have the GDPRModel subclass or GDPRMeta
        """
        with self.assertRaises(Exception):
            register_gdpr_model(ModelWithoutGDPRSubclassOrMeta)
            self.assertNotIn(str(ModelWithoutGDPRSubclassOrMeta._meta), self.mock_registry.models)


class TestRegisterRequireCheckTrueAndNotExcluded(TestCase, GDPRManagerMocks):
    def setUp(self):
        self.setup_settings_mocks({
            "GDPR_MANAGER_EXCLUDE": [],
            "GDPR_MANAGER_REQUIRE_CHECK": True
        })
        self.setup_registry_mocks()

    def test_does_not_error_if_model_has_gdpr_meta_gdpr_subclass_and_meta(self):
        """
        Should not error if the model has the GDPRModel subclass and GDPRMeta
        """
        try:
            register_gdpr_model(ModelWithGDPRMeta)
        except Exception:
            self.fail("Should not fail if GDPR meta has been set")

    def test_errors_if_model_has_no_gdpr_meta(self):
        """
        Should error if the model does not have GDPRMeta
        """
        with self.assertRaises(Exception) as context:
            register_gdpr_model(ModelWithoutGDPRMeta)
        self.assertTrue(
            "Model ModelWithoutGDPRMeta does not have GDPR Manager setup correctly or at all"
            in str(context.exception)
        )

    def test_errors_if_model_has_no_gdpr_subclass(self):
        """
        Should error if model does not have the GDPRModel subclass
        """
        with self.assertRaises(Exception) as context:
            register_gdpr_model(ModelWithoutGDPRSubclass)
        self.assertTrue(
            "Model ModelWithoutGDPRSubclass does not have GDPR Manager setup correctly or at all"
            in str(context.exception)
        )

    def test_errors_if_model_has_no_gdpr_subclass_or_meta(self):
        """
        Should error if model does not have the GDPRModel subclass or GDPRMeta
        """
        with self.assertRaises(Exception) as context:
            register_gdpr_model(ModelWithoutGDPRSubclassOrMeta)
        self.assertTrue(
            "Model ModelWithoutGDPRSubclassOrMeta does not have GDPR Manager setup correctly or at all"
            in str(context.exception)
        )


class TestRegisterExcluded(TestCase, GDPRManagerMocks):
    def setUp(self):
        self.setup_settings_mocks({
            "GDPR_MANAGER_EXCLUDE": ["tests"]
        })
        self.setup_registry_mocks()

    def test_does_not_error_if_model_has_no_gdpr_meta_but_is_excluded(self):
        """
        Shouldn't error if the app the model is contained in is excluded, even if
        they are missing the GDPRMeta class.
        """
        try:
            register_gdpr_model(ModelWithoutGDPRMeta)
        except Exception:
            self.fail("Should not fail if model has been excluded")

    def test_does_not_error_if_model_has_no_gdpr_subclass_but_is_excluded(self):
        """
        Shouldn't error if the app the model is contained in is excluded, even if
        they are missing the GDPR subclass.
        """
        try:
            register_gdpr_model(ModelWithoutGDPRSubclass)
        except Exception:
            self.fail("Should not fail if model has been excluded")

    def test_does_not_error_if_model_has_no_gdpr_subclass_or_meta_but_is_excluded(self):
        """
        Shouldn't error if the app the model is contained in is excluded, even if it is
        missing both the GDPR subclass and the GDPRMeta.
        """
        try:
            register_gdpr_model(ModelWithoutGDPRSubclassOrMeta)
        except Exception:
            self.fail("Should not fail if model has been excluded")

    def test_does_not_register_model_if_has_meta_and_subclass_but_is_excluded(self):
        """
        Shouldn't register the model if the app it is contained in is excluded, even if
        it has been setup correctly with the GDPRModel subclass and GDPRMeta.
        """
        register_gdpr_model(ModelWithGDPRMeta)
        self.assertNotIn(str(ModelWithGDPRMeta._meta), self.mock_registry.models)


class TestRegisterRequireCheckFalse(TestCase, GDPRManagerMocks):
    def setUp(self):
        self.setup_settings_mocks({
            "GDPR_MANAGER_EXCLUDE": [],
            "GDPR_MANAGER_REQUIRE_CHECK": False
        })
        self.setup_registry_mocks()

    def test_register_model_if_has_meta_and_subclass_and_require_check_is_false(self):
        """
        Should register the model if require checks are false if
        it has been setup correctly with the GDPRModel subclass and GDPRMeta.
        """
        register_gdpr_model(ModelWithGDPRMeta)
        self.assertIn(str(ModelWithGDPRMeta._meta), self.mock_registry.models)

    def test_does_not_error_if_model_has_no_gdpr_meta_but_require_check_false(self):
        """
        Shouldn't error if the require check is false, despite missing the GDPRMeta class.
        """
        try:
            register_gdpr_model(ModelWithoutGDPRMeta)
        except Exception:
            self.fail("Should not fail if model has been excluded")

    def test_does_not_error_if_model_has_no_gdpr_subclass_but_require_check_is_false(self):
        """
        Shouldn't error if the require check is false despite missing the GDPR subclass.
        """
        try:
            register_gdpr_model(ModelWithoutGDPRSubclass)
        except Exception:
            self.fail("Should not fail if model has been excluded")

    def test_does_not_error_if_model_has_no_gdpr_subclass_or_meta_but_require_check_is_false(self):
        """
        Shouldn't error if the require check is false, despite missing the GDPR subclass and the GDPRMeta.
        """
        try:
            register_gdpr_model(ModelWithoutGDPRSubclassOrMeta)
        except Exception:
            self.fail("Should not fail if model has been excluded")
