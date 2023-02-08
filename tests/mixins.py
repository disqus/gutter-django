import django
from exam import before
from django.apps import apps

class SetupDjangoTest(object):

    @before
    def setup_django(self):
        # For Django 1.7+, we need to run `django.setup()` first.

        if hasattr(django, 'setup'):
            if not apps.ready and not apps.loading:
                django.setup()
