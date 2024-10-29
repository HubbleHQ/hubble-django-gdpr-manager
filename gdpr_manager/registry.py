class Registry(object):
    def __init__(self):
        # Register models with privacy meta
        self.models = {}

    def register(self, model):
        """
        Register a model so that we can search it
        """
        self.models[str(model._meta)] = model

    def search(self, **search_data):
        """
        Search the registry's models for a given term
        """
        full_results = []
        for key, model in self.models.items():
            results = model.gdpr_search(**search_data)
            if results:
                full_results.append((model, results))

        return full_results


gdpr_registry = Registry()
