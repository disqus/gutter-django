import unittest

from exam.cases import Exam

from gutter.web import autodiscover

from describe import expect


class WebTest(Exam, unittest.TestCase):

    def test_autodiscover_is_autodiscovery_discover(self):
        from gutter.web.autodiscovery import discover
        expect(autodiscover).to.be_equal_to(discover)
