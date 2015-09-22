import unittest2

from django.http import HttpRequest
from exam import Exam, fixture, before

from .mixins import SetupDjangoTest

ROOT_URLCONF = 'example_project.urls'


class TestGutterModule(SetupDjangoTest, Exam, unittest2.TestCase):

    @fixture
    def request(self):
        req = HttpRequest()
        req.path = '/gutter'
        return req

    @before
    def ensure_nexus_module_registered(self):
        from gutter.django import nexus_modules  # NOQA

    @fixture
    def module(self):
        import nexus
        return nexus.site.get_module('gutter')

    def test_index_works(self):
        self.module.index(self.request)
