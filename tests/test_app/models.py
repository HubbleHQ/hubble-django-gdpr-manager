from django.db import models
from gdpr_manager.models import GDPRModel

class ModelWithGDPRMeta(models.Model, GDPRModel):
    """
    Correctly setup; GDPR meta with subclass and meta
    """

    chars = models.CharField(max_length=255)
    email = models.EmailField()
    user_id = models.IntegerField()

    class GDPRMeta:
        fields = ["chars", "email"]
        search_user_id_fields = ["user_id"]
        search_email_fields = ["email"]


class ModelWithoutGDPRMeta(models.Model, GDPRModel):
    """
    Incorrectly setup; without GDPR meta
    """

    chars = models.CharField(max_length=255)
    email = models.EmailField()


class ModelWithoutGDPRSubclass(models.Model):
    """
    Incorrectly setup; with GDPRmeta but without GDPR Subclass
    """

    chars = models.CharField(max_length=255)
    email = models.EmailField()
    user_id = models.IntegerField()

    class GDPRMeta:
        fields = ["chars", "email"]
        search_user_id_fields = ["user_id"]
        search_email_fields = ["email"]


class ModelWithoutGDPRSubclassOrMeta(models.Model):
    """
    Incorrectly setup; without GDPR meta and GDPR subclass
    """

    chars = models.CharField(max_length=255)
    email = models.EmailField()