import unittest2

from exam.cases import Exam

from gutter.django import autodiscover


class WebTest(Exam, unittest2.TestCase):

    def test_autodiscover_is_autodiscovery_discover(self):
        from gutter.django.autodiscovery import discover
        self.assertEquals(autodiscover, discover)
