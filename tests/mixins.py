import django
from django.conf import settings
from exam import before, after


class SetupDjangoTest(object):

    @before
    def setup_django(self):
        # For Django 1.7+, we need to run `django.setup()` first.
        if hasattr(django, 'setup'):
            django.setup()

    # @after
    # def undo_setup_django(self):
    #     if hasattr(django, 'setup'):
    #         settings.INSTALLED_APPS = self.__original_installed_apps
    #         del self.__original_installed_apps
