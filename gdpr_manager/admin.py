from django.contrib import admin
from django.db import models
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django import forms
from django.contrib.contenttypes.models import ContentType

from .registry import gdpr_registry
from . import settings

csrf_protect_m = method_decorator(csrf_protect)


class GDPRManager(models.Model):
    """
    Fake model to make this project appear in the admin without intrusive hacks
    """

    class Meta:
        managed = False
        verbose_name_plural = "GDPR Manager"


class GDPRManagerSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for search_type in settings.GDPR_MANAGER_SEARCH_TYPES:
            field_name = search_type["key"]
            display_name = search_type["verbose_name"]
            self.fields[field_name] = forms.CharField(
                label=display_name, max_length=255, required=False
            )


class GDPRManagerAdmin(admin.ModelAdmin):
    change_list_template = "gdpr_manager/admin/gm_change_list.html"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request):
        return False

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        """
        The replacement view to manage PII
        """
        form = GDPRManagerSearchForm(request.POST or None)
        results = None

        if form.is_valid():
            search_data = {}
            for search_type in settings.GDPR_MANAGER_SEARCH_TYPES:
                search_data[search_type["key"]] = form.cleaned_data[search_type["key"]]

            raw_results = gdpr_registry.search(**search_data)

            results = (
                {
                    "model": model,
                    "results": model_results,
                    "app_label": model._meta.app_label,
                    "name": model._meta.verbose_name,
                    "content_type": ContentType.objects.get_for_model(model),
                    "url_name": "admin:{}_{}_change".format(
                        model._meta.app_label, model._meta.model_name
                    ),
                    "url_change_name": "admin:{}_{}_changelist".format(
                        model._meta.app_label, model._meta.model_name
                    ),
                }
                for model, model_results in raw_results
            )

        return render(
            request,
            self.change_list_template,
            {"title": "GDPR Manager", "form": form, "results": results},
        )


admin.site.register(GDPRManager, GDPRManagerAdmin)
