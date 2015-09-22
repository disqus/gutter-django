import django
from django.conf import settings
from exam import before


class SetupDjangoTest(object):

    @before
    def setup_django(self):
        # For Django 1.7+, we need to run `django.setup()` first.
        if hasattr(django, 'setup'):
            settings.INSTALLED_APPS = (
                'django.contrib.auth',
                'django.contrib.sessions',
            ) + settings.INSTALLED_APPS
            django.setup()
