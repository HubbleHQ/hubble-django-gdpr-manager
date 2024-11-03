from unittest import mock

from django.test import TestCase

from gdpr_manager.handlers import check_search_types

from .helpers import GDPRManagerMocks
from .models import (
    ModelWithSingleFieldsToSearch,
    ModelWithMultipleFieldsToSearch,
    ModelWithCustomSearchNotesField,
    ModelWithShowWarningIfFoundTrue,
    ModelWithShowWarningIfFoundFalse
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
        ModelWithSingleFieldsToSearch.objects.create(email="test@test.com", user_id=143)
        ModelWithSingleFieldsToSearch.objects.create(email="hamster@carrot.com", user_id=6783)

        (results, has_warning) = ModelWithSingleFieldsToSearch.gdpr_search(user_id=987)

        self.assertEqual(len(results), 0)

    def test_search_by_multiple_search_types_at_once(self):
        """
        You should be able to search by multiple search types at once
        and it return any results that match either search type.
        """
        ModelWithSingleFieldsToSearch.objects.create(email="test@test.com", user_id=143)
        ModelWithSingleFieldsToSearch.objects.create(email="test@test1.com", user_id=143)
        ModelWithSingleFieldsToSearch.objects.create(email="hamster@carrot.com", user_id=6783)

        (results, has_warning) = ModelWithSingleFieldsToSearch.gdpr_search(
            user_id=143, email="hamster@carrot.com"
        )

        self.assertEqual(len(results), 3)

    def test_should_search_ignoring_casing(self):
        """
        The search should ignore any casing and return results
        even if it does not match
        """
        ModelWithSingleFieldsToSearch.objects.create(email="test@test.com", user_id=178)
        ModelWithSingleFieldsToSearch.objects.create(email="test@TEST.com", user_id=92)

        (results, has_warning) = ModelWithSingleFieldsToSearch.gdpr_search(
            email="test@test.com"
        )

        self.assertEqual(len(results), 2)

    def test_search_multiple_fields(self):
        """
        Should search all fields listed in GDPRMeta for a search type, 
        not just one of them.
        """
        ModelWithMultipleFieldsToSearch.objects.create(
            email="test0@test.com", user_id=345, host_id=956
        )
        ModelWithMultipleFieldsToSearch.objects.create(
            email="test1@test.com", user_id=1967, host_id=345
        )
        ModelWithMultipleFieldsToSearch.objects.create(
            email="test2@test.com", user_id=1967, host_id=956
        )

        (results, has_warning) = ModelWithMultipleFieldsToSearch.gdpr_search(user_id=345)

        self.assertEqual(len(results), 2)

    def test_should_do_custom_search_if_double_underscore_in_field_name(self):
        """
        iexact is the default but not the only search you can do
        if you pass in name__icontains for example it should do a contains
        search instead of an iexact search. This is super useful for things
        like searching notes fields.
        """
        ModelWithCustomSearchNotesField.objects.create(
            email="somerandom@email.com",
            user_id=74821,
            notes=(
                "These are some notes of a very boring kind with\n",
                "an email somewhere in here MOHAHAHA\n"
                "banana@fridge.com is the email\n"
                "let us keep it hidden so noone can find it!"
            )
        )
        ModelWithCustomSearchNotesField.objects.create(
            email="someotherrandom@email.com",
            user_id=92893,
            notes=(
                "This is another very boring note with lovely\n",
                "email addresses in it:baNaNa@fridge.com0783928\n"
                "lets try even harder to hide that email!"
            )
        )
        ModelWithCustomSearchNotesField.objects.create(
            email="ainteresting@email.com",
            user_id=81839,
            notes=(
                "This a very interesting note with with a\n",
                "decoy email address in it! banana@fridge-hammer.com0783928\n"
                "I love to try and confuse people as much as I can!"
            )
        )

        (results, has_warning) = ModelWithCustomSearchNotesField.gdpr_search(email="banana@fridge.com")
        self.assertEqual(len(results), 2)

    def test_return_has_warning_true_if_show_warning_if_found(self):
        """
        If show_warning_if_found is True on the GDPRMeta then it should return
        has warning as True
        """
        ModelWithShowWarningIfFoundTrue.objects.create(email="test@test.com", user_id=143)

        (results, has_warning) = ModelWithShowWarningIfFoundTrue.gdpr_search(email="test@test.com")
        self.assertTrue(has_warning)

    def test_return_has_warning_false_if_no_search_results(self):
        """
        If there are no search results then it should return
        has warning as False
        """
        ModelWithShowWarningIfFoundTrue.objects.create(email="test@test.com", user_id=143)

        (results, has_warning) = ModelWithShowWarningIfFoundTrue.gdpr_search(email="404@email.com")
        self.assertFalse(has_warning)

    def test_return_has_warning_false_if_show_warning_if_found_false(self):
        """
        If show_warning_if_found is False on the GDPRMeta then it should return
        has warning as False
        """
        ModelWithShowWarningIfFoundFalse.objects.create(email="test@test.come", user_id=143)
        (results, has_warning) = ModelWithShowWarningIfFoundFalse.gdpr_search(email="test@test.com")
        self.assertFalse(has_warning)

    def test_return_has_warning_false_if_no_show_warning_if_found(self):
        """
        If show_warning_if_found is has not been set on GDPRMeta then it should return
        has warning as False
        """
        ModelWithSingleFieldsToSearch.objects.create(email="test@test.come", user_id=143)
        (results, has_warning) = ModelWithSingleFieldsToSearch.gdpr_search(email="test@test.com")
        self.assertFalse(has_warning)