import unittest2

from exam.cases import Exam
from exam.helpers import mock_import

from gutter.django.autodiscovery import discover

from nose.tools import *


class AutodiscoverTest(Exam, unittest2.TestCase):

    def run(self, *args, **kwargs):
        # Have to do this mock_import gymnastics because the imports inside the
        # autodiscovery module are local imports
        with mock_import('django.conf.settings') as mock_settings:
            mock_settings.INSTALLED_APPS = ['foo.bar']

            with mock_import('importlib.import_module') as im:
                self.import_module = im
                super(AutodiscoverTest, self).run(*args, **kwargs)

    def test_autodiscover_attempts_to_import_gutter_in_installed_apps(self):
        discover()
        self.import_module.assert_called_once_with('foo.bar.gutter')

    def test_fails_silently_if_import_does_not_exist(self):
        self.import_module.side_effect = ImportError
        discover()  # No exception raised means it worked
