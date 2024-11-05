from django.db.models import Q

from .helpers import get_search_type_definition

"""
This model does not inherit from django models,
if it did it would break the signals we have to check
if the model has been instantiated correctly.

DO NOT add a model in here that uses a django model.
"""

class GDPRModel:
    @classmethod
    def gdpr_search(cls, **search_data):
        query = Q()
        results = []
        has_warning = False

        for key, value in search_data.items():
            if not value:
                # Breaks icontains lookup if you search an empty value
                break

            search_fields = getattr(cls.GDPRMeta, f"search_{key}_fields")
            search_type_def = get_search_type_definition(key)

            for field_name in search_fields:
                search_field_query = cls.gdpr_search_field_query(
                    field_name=field_name,
                    value=value,
                    search_type=search_type_def
                )
                query.add(Q(**search_field_query), Q.OR)

        ## Don't run if there is no query as it gets ... everything
        if len(query):
            results = cls.objects.filter(query)

        if len(results):
            has_warning = getattr(
                cls.GDPRMeta,
                "show_warning_if_found",
                False
            )
            
        return (results, has_warning)
    
    @classmethod
    def gdpr_search_field_query(cls, field_name, value, search_type):
        if "__" not in field_name:
            # In the future will want to be able to modify this, 
            # search by a regex for searching notes for example
            lookup = search_type.get("default_lookup", "iexact")
            field_name = f"{field_name}__{lookup}"

        search_field_query = {field_name: value}
        return search_field_query