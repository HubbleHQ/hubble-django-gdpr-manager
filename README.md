
Hubble Django GDPR Manager
=====

Package to handle hubbles GDPR data within Django. At the moment this adds an admin page which allows you to search by key user data to get the information needed.

Contents
----
- [Quick Start](#quick-start)
- [Example](#example)
- [Searching Fields](#searching-fields)
- [Settings](#settings)
- [Contributing Guide](#contributing-guide)
    - [Important note on adding packages](#important-note-on-adding-packages)
    - [Setup within another project](#setup-within-another-project)
    - [Deploying to PyPi](#deploying-to-pypi)

Quick start
-----------
1. Install "hubble-django-gdpr-manager" from pip

1. Add "gdpr_manager" to your INSTALLED_APPS setting like this:
    ```
    INSTALLED_APPS = [
        ...,
        "gdpr_manager",
    ]
    ```

2. You will get alot of errors turn up, you need to go through each model one by one and either set it up to use the GDPR manager or in the case of it being a third party package, add it to the exclude list.

Example
-----------
```python
from gdpr_manager.models import GDPRModel

class ExampleModel(models.Model, GDPRModel):
    ...
    class GDPRMeta:
        fields=['Any model fields containing personal data']
        search_user_id_fields=['model fields that can be used to search by User ID']
        search_email_fields=['model fields that can be used to search by Email']
        """
        Will show a warning that the GDPR request needs to be treated
        differently & to talk to the person managing the request
        if data is found in this table
        """
        show_warning_if_found=[True|False optional]
    ...
```

Searching Fields
----------
By default all searches are done by using the `default_lookup` value defined in [GDPR_MANAGER_SEARCH_TYPES](#settings). The `default_lookup` is then appended to the field name when searching so `email` becomes `email__iexact` for example.

If you want to do a custom search using another [field lookup](https://docs.djangoproject.com/en/5.1/ref/models/querysets/#field-lookups) then when you add the field name you can add the field lookup to the field name.
```python
# Here it will return any notes fields with the email somewhere in it
search_email_fields=['email', 'notes__icontains']

# Eventual query builder
query.add(Q(email_iexact=email), Q.OR)
query.add(Q(notes__icontains=email). Q.OR)
```

Settings
-----------
To override put these variables in your main apps `settings.py` file

`GDPR_MANAGER_REQUIRE_CHECK` <br>
Default: `True`

Allows you to turn off the very loud check that crashes the server every time it meets a model that doesn't have the GDPR manager setup correctly.

This can be useful when adding to a legacy project, however the errors can also be very useful to make sure you haven't missed anything.

**This setting should be used in setup or debugging only**

`GDPR_MANAGER_EXCLUDE` <br>
Default: `[]`

Allows you to exclude django apps from being checked and managed by the GDPR manager. This is very beneficial when it comes to third-party apps.

You would need a very good reason to exclude an app we manage from the GDPR manager.

`GDPR_MANAGER_EXCLUDE_MODELS` <br>
Default: `[]`

Allows you to exclude specific models from being checked and managed by the GDPR manager. This is very beneficial when it comes to join tables that we do not control being created, but you do not want to exclude the whole app.

`GDPR_MANAGER_SEARCH_TYPES` <br>
Default:
```
[
    {
        "key": "user_id", 
        "verbose_name": "User ID",
        "default_lookup": "exact"
    },
    {
        "key": "email",
        "verbose_name": "Email",
        "default_lookup": "iexact"
    },
]
```

A way of managing the fields that can be searched on the admin page. In most cases `user_id` and `email` is enough but organisation id for example might need searching (pass).

The default lookup relates to the [field lookup](https://docs.djangoproject.com/en/5.1/ref/models/querysets/#field-lookups) the search uses. If none is set it will default to `iexact`.

NOTE: `iexact` cannot be used on foreign key searches for example thus the option to do an exact search.

`GDPR_MANAGER_EXCLUDE_DEFAULT` <br>
Default:
```
[
    "django",
    "__fake__",
    "rest_framework",
    "gdpr_manager",
    "django_rq",
]
```
This is the core list of packages that are excluded by default, I do not think there is a case to override these values however left this information here so ya'll know. Plus you never know what the future brings.

Contributing Guide
-----------
The best way to work on this package is to import it into another django project so you can play with the two together. It's much easier.

### Important note on adding packages
The files in the Pipfile are not dependancies for the package.
[To add dependancies you need to add them into the setup.cfg.](
https://setuptools.pypa.io/en/latest/userguide/dependency_management.html#declaring-required-dependency)
Make sure to follow the `setup.cfg` tab, not the `.toml` one, it will break and get angry.


### Setup within another project
1. Go to the project you want to import the package into for testing.
2. In the `docker-compose.yml` add an additional context pointing at your local download of this package.
    ```yaml
    dev:
        ...
        build:
            ...
            additional_contexts:
                - gdpr_manager=~/local/path/hubble-django-gdpr-manager
        ...
    dev-worker:
        [if there is a dev-worker, do the same here as above]
    ```
3. In the `Dockerfile` add the gdpr manager package by copying its files into its own directory and then installing it using a pip local directory install.

    The `-e` means editable which allows us to work on the package without reinstalling or rebuilding every time we make a change (its magic!).

    ```Dockerfile
    # Create directory not in /src to copy the package to
    RUN mkdir /hubble-django-gdpr-manager
    # Copy the package from the additional context we setup before into the container
    COPY --from=gdpr_manager . /hubble-django-gdpr-manager
    # Install the local package with the editable flag
    RUN python -m pip install -e /hubble-django-gdpr-manager
    ```

4. In `docker-compose.common.yml` add the `/hubble-django-gdpr-manager` we created in the container to our local folder so it can update as we edit it.
    ```yaml
    services:
        [service_name]_base:
            ...
            volumes:
                ...
                - ~/local/path/hubble-django-gdpr-manager:/django-gdpr-manager
            ...
    ```
5. Add "gdpr_manager" to your INSTALLED_APPS setting like this:
    ```
    INSTALLED_APPS = [
        ...,
        "gdpr_manager",
    ]
    ```
6. Build and run the service you are testing with and you should have a live updating package you can test with.

    Easiest way to test is to go into the `templates/gdpr_manager/gm_change_list.html` and add some random text and see if it shows up in the admin.


### Deploying to PyPi


1. Ensure you're listed as a contributing member for the package in Pypi and if you want to do a test deploy in test PyPi as well. They use separate users, so you may need to sign up again. We don't seem to use organisations in PyPi so you need adding to the project directly.
2. Update the version number in `pyproject.toml` use semantic version as it makes sense, e.g. minor version changes for minor updates
3. Run `make build` to get a build - you don't need to anything with this version but look in the `dist/` directory to make sure the version and name all look correct.
4. Run `make test-deploy` this will build and attempt an upload to the test PyPi
 1. Before being uploaded it will ask you to enter a token.
 2. To generate a token go to https://test.pypi.org/, login -> account settings -> scroll down -> api tokens -> generate a new one with access to the project. If you don't see the project then go back to point 1.
 3. Copy the token into the prompt from `make test-deploy`
 4. Check test pypi has the updated version.
5. Run `make deploy` for a production release and follow the same steps as the test but on the proper PyPi.
