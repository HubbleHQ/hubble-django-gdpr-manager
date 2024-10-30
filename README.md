
Django GDPR Manager
=====

Package to handle hubbles GDPR data within Django. At the moment this adds an admin page which allows you to search by key user data to get the information needed.

Contents
----
- [Quick Start](#quick-start)
- [Example](#example)
- [Settings](#settings)
- [Contributing Guide](#contributing-guide)
    - [Setup within another project](#setup-within-another-project)

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
```
from gdpr_manager.models import GDPRModel

class ExampleModel(models.Model, GDPRModel):
    ...
    class GDPRMeta:
        fields=['Any model fields containing personal data']
        search_user_id_fields=['model fields that can be used to search by User ID']
        search_email_fields=['model fields that can be used to search by Email']
    ...
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

`GDPR_MANAGER_SEARCH_TYPES` <br>
Default:
```
[
    {"key": "user_id", "verbose_name": "User ID"},
    {"key": "email", "verbose_name": "Email"},
]
```

A way of managing the fields that can be searched on the admin page. In most cases `user_id` and `email` is enough but organisation id for example might need searching (pass).

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

**Right now this project does not have working tests, that is something that needs setting up.**

### Setup within another project
1. Go to the project you want to import the package into for testing.
2. In the `docker-compose.yml` add an additional context pointing at your local download of this package.
    ```yaml
    dev:
        ...
        build:
            ...
            additional_contexts:
                - gdpr_manager=~/local/path/django-gdpr-manager
        ...
    dev-worker:
        [if there is a dev-worker, do the same here as above]
    ```
3. In the `Dockerfile` add the gdpr manager package by copying its files into its own directory and then installing it using a pip local directory install. 

    The `-e` means editable which allows us to work on the package without reinstalling or rebuilding every time we make a change (its magic!).

    ```Dockerfile
    # Create directory not in /src to copy the package to
    RUN mkdir /django-gdpr-manager
    # Copy the package from the additional context we setup before into the container
    COPY --from=gdpr_manager . /django-gdpr-manager
    # Install the local package with the editable flag
    RUN python -m pip install -e /django-gdpr-manager
    ```

4. In `docker-compose.common.yml` add the `/django-gdpr-manager` we created in the container to our local folder so it can update as we edit it.
    ```yaml
    services:
        [service_name]_base:
            ...
            volumes:
                ...
                - ~/local/path/django-gdpr-manager:/django-gdpr-manager
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
