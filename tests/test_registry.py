import unittest

from gutter.web import registry

from gutter.client.operators.comparable import *
from gutter.client.operators.identity import *
from gutter.client.operators.misc import *

from describe import expect

from exam import Exam, before, fixture

from mock import sentinel


class TestRegistry(Exam, unittest.TestCase):

    @fixture
    def default_operator_list(self):
        return list((Equals, Between, LessThan, LessThanOrEqualTo, MoreThan,
                MoreThanOrEqualTo, Truthy, Percent, PercentRange))

    @before
    def reload_module(self):
        reload(registry)

    def test_operators_starts_out_with_default_list(self):
        expect(registry.operators).to == self.default_operator_list

    def test_can_append_to_operators(self):
        expect(registry.operators).to_not.contain(sentinel.operator)
        registry.operators.append(sentinel.operator)
        expect(registry.operators).to.contain(sentinel.operator)

    def test_arguments_starts_out_empty(self):
        expect(registry.arguments).to == []

