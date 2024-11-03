from django.db import models
from gdpr_manager.models import GDPRModel

"""
Registry tests
"""
class ModelWithGDPRMeta(models.Model, GDPRModel):
    """
    Correctly setup; GDPR meta with subclass and meta
    """
    some_personal_info = models.CharField(max_length=255)
    email = models.EmailField()
    user_id = models.IntegerField()


    class GDPRMeta:
        fields = ["some_personal_info", "email"]
        search_user_id_fields = ["user_id"]
        search_email_fields = ["email"]

class ModelWithoutGDPRMeta(models.Model, GDPRModel):
    """
    Incorrectly setup; without GDPR meta
    """

    some_personal_info = models.CharField(max_length=255)
    email = models.EmailField()


class ModelWithoutGDPRSubclass(models.Model):
    """
    Incorrectly setup; with GDPRmeta but without GDPR Subclass
    """

    some_personal_info = models.CharField(max_length=255)
    email = models.EmailField()
    user_id = models.IntegerField()

    class GDPRMeta:
        fields = ["some_personal_info", "email"]
        search_user_id_fields = ["user_id"]
        search_email_fields = ["email"]


class ModelWithoutGDPRSubclassOrMeta(models.Model):
    """
    Incorrectly setup; without GDPR meta and GDPR subclass
    """

    some_personal_info = models.CharField(max_length=255)
    email = models.EmailField()

"""
Search Tests
"""
class ModelWithSingleFieldsToSearch(models.Model, GDPRModel):
    """
    Basic model with only simple, single fields to search
    """
    email = models.EmailField()
    user_id = models.IntegerField()

    class GDPRMeta:
        fields = ["email"]
        search_user_id_fields = ["user_id"]
        search_email_fields = ["email"]

class ModelWithMultipleFieldsToSearch(models.Model, GDPRModel):
    """
    Model with multiple fields to search for one search type
    all fields are kept simple
    """
    email = models.EmailField()
    user_id = models.IntegerField()
    host_id = models.IntegerField()

    class GDPRMeta:
        fields = ["email"]
        search_user_id_fields = ["user_id", "tenant_id"]
        search_email_fields = ["email"]

class ModelWithCustomSearchNotesField(models.Model, GDPRModel):
    """
    Model with a custom search notes field searching by icontains
    """
    email = models.EmailField()
    user_id = models.IntegerField()
    notes = models.TextField()

    class GDPRMeta:
        fields = ["email", "notes"]
        search_user_id_fields = ["user_id"]
        search_email_fields = ["email", "notes__icontains"]