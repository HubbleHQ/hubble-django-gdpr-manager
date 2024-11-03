from unittest import mock

from django.test import TestCase

from gdpr_manager.handlers import check_search_types

from .helpers import GDPRManagerMocks
from .models import (
    ModelWithSingleFieldsToSearch,
    ModelWithMultipleFieldsToSearch,
    ModelWithCustomSearchNotesField
)


class TestGDPRSearch(TestCase, GDPRManagerMocks):
    def setUp(self):
        self.setup_registry_mocks()

    def test_search_by_a_single_search_type(self):
        """
        You should be able to search by a single search type
        and get results if the model has the data you have searched by
        """
        ModelWithSingleFieldsToSearch.objects.create(email="test@test.com", user_id=143)
        ModelWithSingleFieldsToSearch.objects.create(email="test@test1.com", user_id=143)
        ModelWithSingleFieldsToSearch.objects.create(email="hamster@carrot.com", user_id=6783)

        (results, has_warning) = ModelWithSingleFieldsToSearch.gdpr_search(user_id=143)

        self.assertEqual(len(results), 2)

    def test_search_by_a_single_search_type_no_results(self):
        """
        You should be able to search by a single search type
        and get an empty list if the model does not have the data
        you are searching by.
        """
        pass

    def test_search_by_multiple_search_types_at_once(self):
        """
        You should be able to search by multiple search types at once
        and it return any results that match either search type.
        """
        pass

    def test_search_by_multiple_search_types_no_results(self):
        """
        You should be able to search by a multiple search types
        and get an empty list if the model does not have the data
        you are searching by.
        """
        pass

    def test_search_multiple_fields(self):
        """
        Should search all fields listed in GDPRMeta for a search type, 
        not just one of them.
        """
        pass

    def test_should_search_ignoring_casing(self):
        """
        The search should ignore any casing and return results
        even if it does not match
        """
        pass

    def test_should_do_custom_search_if_double_underscore_in_field_name(self):
        """
        iexact is the default but not the only search you can do
        if you pass in name__icontains for example it should do a contains
        search instead of an iexact search. This is super useful for things
        like searching notes fields.
        """
        pass