import unittest

from nose.tools import *

from gutter.web import registry

from gutter.client.operators.comparable import *
from gutter.client.operators.identity import *
from gutter.client.operators.misc import *
from gutter.client import arguments

from describe import expect

from exam import Exam, before, fixture

from mock import sentinel


class FooArgs(arguments.Container):
    a = arguments.String('a')
    b = arguments.String('a')


class BarArgs(arguments.Container):
    a = arguments.String('a')
    b = arguments.String('a')


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

    def test_operators_to_choices_returns_suitable_tuple(self):
        eq_(
            registry.operators.as_choices,
            [
                (
                    'Comparable', [
                        ('equals', 'Equal To'),
                        ('between', 'Between'),
                        ('before', 'Less Than'),
                        ('less_than_or_equal_to', 'Less Than Or Equal To'),
                        ('more_than', 'More Than'),
                        ('more_than_or_equal_to', 'More Than Or Equal To')
                    ]
                ),
                (
                    'Misc', [
                        ('percent', 'Within The Percentage Of'),
                        ('percent_range', 'In The Percentage Range Of')
                    ]
                ),
                (
                    'Identity', [
                        ('true', 'True')
                    ]
                )
            ]
        )

    def test_arguments_as_choices_returns_suiteable_tuple(self):
        registry.arguments.append(FooArgs.a)
        registry.arguments.append(FooArgs.b)
        registry.arguments.append(BarArgs.a)
        registry.arguments.append(BarArgs.b)

        eq_(
            registry.arguments.as_choices,
            [
                (
                    'FooArgs', [
                        ('FooArgs.a', 'FooArgs.a'),
                        ('FooArgs.b', 'FooArgs.b')
                    ]
                ),
                (
                    'BarArgs', [
                        ('BarArgs.a', 'BarArgs.a'),
                        ('BarArgs.b', 'BarArgs.b')
                    ]
                )
            ]
        )
