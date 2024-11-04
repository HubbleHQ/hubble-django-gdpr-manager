from unittest import mock
from django.test import TestCase

from .helpers import GDPRManagerMocks
from .models import (
    ModelWithGDPRMeta,
    ModelWithSingleFieldsToSearch
)

class TestRegistryRegister(TestCase, GDPRManagerMocks):
    def setUp(self):
        self.setup_registry_mocks()

    def test_add_model_to_models_list(self):
        self.mock_registry.register(ModelWithGDPRMeta)

        self.assertIn(str(ModelWithGDPRMeta._meta), self.mock_registry.models)


class TestRegistrySearch(TestCase, GDPRManagerMocks):
    def setUp(self):
        self.setup_registry_mocks()
    
    @mock.patch.object(ModelWithGDPRMeta, 'gdpr_search', return_value=([], False))
    @mock.patch.object(ModelWithSingleFieldsToSearch, 'gdpr_search', return_value=([], False))
    def test_calls_gdpr_search_on_all_models(self, model1_gdpr_search, model2_gdpr_search):
        """
        It should call gdpr_search on all models
        """
        self.mock_registry.register(ModelWithGDPRMeta)
        self.mock_registry.register(ModelWithSingleFieldsToSearch)

        self.mock_registry.search(user_id=1)

        model1_gdpr_search.assert_called_once()
        model2_gdpr_search.assert_called_once()

    @mock.patch.object(ModelWithGDPRMeta, 'gdpr_search', return_value=([], False))
    @mock.patch.object(ModelWithSingleFieldsToSearch, 'gdpr_search', return_value=([], False))
    def test_passes_search_params_to_all_models(self, model1_gdpr_search, model2_gdpr_search):
        """
        It should pass the search params down to the models it is searching
        """
        self.mock_registry.register(ModelWithGDPRMeta)
        self.mock_registry.register(ModelWithSingleFieldsToSearch)

        self.mock_registry.search(user_id=1, email="hi@email.com")

        model1_gdpr_search.assert_called_with(user_id=1, email="hi@email.com")
        model2_gdpr_search.assert_called_with(user_id=1, email="hi@email.com")

    @mock.patch.object(ModelWithGDPRMeta, 'gdpr_search', return_value=(["hi"], False))
    @mock.patch.object(ModelWithSingleFieldsToSearch, 'gdpr_search', return_value=(["yay"], False))
    def test_includes_models_if_has_results(self, model1_gdpr_search, model2_gdpr_search):
        """
        It should include a model if the model
        return anything when it searches
        """
        self.mock_registry.register(ModelWithGDPRMeta)
        self.mock_registry.register(ModelWithSingleFieldsToSearch)

        full_results = self.mock_registry.search(
            user_id=1, email="hi@email.com"
        )
        
        # Returns a tuple with model, results and has_warning
        self.assertEqual(len(full_results), 2)

    @mock.patch.object(ModelWithGDPRMeta, 'gdpr_search', return_value=(["hi"], False))
    @mock.patch.object(ModelWithSingleFieldsToSearch, 'gdpr_search', return_value=([], False))
    def test_excludes_model_if_no_results(self, model1_gdpr_search, model2_gdpr_search):
        """
        It should exclude a model from the results if the model doesn't
        return anything when it searches
        """
        self.mock_registry.register(ModelWithGDPRMeta)
        self.mock_registry.register(ModelWithSingleFieldsToSearch)

        full_results = self.mock_registry.search(
            user_id=1, email="hi@email.com"
        )
        
        # Returns a tuple with model, results and has_warning
        self.assertEqual(len(full_results), 1)
    
    @mock.patch.object(ModelWithGDPRMeta, 'gdpr_search', return_value=(["hi"], False))
    @mock.patch.object(ModelWithSingleFieldsToSearch, 'gdpr_search', return_value=(["yay"], False))
    def test_returns_list_with_models_and_results(self, model1_gdpr_search, model2_gdpr_search):
        """
        It should return a list of models with results
        """
        self.mock_registry.register(ModelWithGDPRMeta)
        self.mock_registry.register(ModelWithSingleFieldsToSearch)

        full_results = self.mock_registry.search(
            user_id=1, email="hi@email.com"
        )
        
        # Returns a tuple with model, results and has_warning
        self.assertEqual(full_results[0][0], ModelWithGDPRMeta)
        self.assertEqual(full_results[0][1], ["hi"])
        self.assertEqual(full_results[1][0], ModelWithSingleFieldsToSearch)
        self.assertEqual(full_results[1][1], ["yay"])

    @mock.patch.object(ModelWithGDPRMeta, 'gdpr_search', return_value=(["hi"], True))
    def test_returns_warning_true_if_has_warning(self, model1_gdpr_search):
        self.mock_registry.register(ModelWithGDPRMeta)
        
        full_results = self.mock_registry.search(
            user_id=1, email="hi@email.com"
        )

        self.assertEqual(full_results[0][2], True)

    @mock.patch.object(ModelWithGDPRMeta, 'gdpr_search', return_value=(["hi"], False))
    def test_returns_warning_false_if__has_warning_false(self, model1_gdpr_search):
        self.mock_registry.register(ModelWithGDPRMeta)
        
        full_results = self.mock_registry.search(
            user_id=1, email="hi@email.com"
        )

        self.assertEqual(full_results[0][2], False)





        
