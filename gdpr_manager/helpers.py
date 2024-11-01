from . import settings


def gdpr_meta_example(missing_keys=None, model_name="ExampleModel"):
    exception_key_example = []

    for search_type in settings.GDPR_MANAGER_SEARCH_TYPES:
        example_string = (
            "        "
            f"search_{search_type['key']}_fields=['model fields that can be used"
            f" to search by {search_type['verbose_name']}']"
        )

        if not missing_keys:
            exception_key_example.append(example_string)
        elif f"search_{search_type['key']}_fields" in missing_keys:
            exception_key_example.append(example_string)

    # can't use a backslash in a f"" string
    exception_key_example_string = "\n".join(exception_key_example)

    missing_keys_example = (
        f"class {model_name}(models.Model, GDPRModel):\n"
        "    ...\n"
        "    class GDPRMeta:\n"
        "        ... \n"
        f"{exception_key_example_string}"
    )
    full_example = (
        f"class {model_name}(models.Model, GDPRModel):\n"
        "    ...\n"
        "    class GDPRMeta:\n"
        "        fields=['Any model fields containing personal data']\n"
        f"{exception_key_example_string}\n"
        "        \"\"\"\n"
        "        Will show a warning that the GDPR request needs to be treated\n"
        "        differently & to talk to the person managing the request\n"
        "        if data is found in this table\n"
        "        \"\"\"\n"
        "        show_warning_if_found=[True|False optional]"
    )

    return missing_keys_example if missing_keys else full_example


def gdpr_subclass_example(model_name="ExampleModel", with_meta_example=False):
    import_example = "from gdpr_manager.models import GDPRModel\n\n"

    if not with_meta_example:
        return (
            "\033[1mExample:\033[0m \n"
            f"{import_example}"
            f"class {model_name}(models.Model, GDPRModel):\n"
            "    ..."
        )
    else:
        return (
            "\033[1mExample:\033[0m \n"
            f"{import_example}"
            f"{gdpr_meta_example(model_name=model_name)}"
        )
