from django.db.models import Q

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
            search_fields = getattr(cls.GDPRMeta, f"search_{key}_fields")
            for field_name in search_fields:
                if "__" not in field_name:
                    # In the future will want to be able to modify this, 
                    # search by a regex for searching notes for example
                    field_name = "{}__iexact".format(field_name)
                search_term_query = {field_name: value}
                query.add(Q(**search_term_query), Q.OR)

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
