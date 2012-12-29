import unittest2

from nose.tools import *

from gutter.django import registry

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


class TestRegistry(Exam, unittest2.TestCase):

    @fixture
    def default_operator_dict(self):
        operators = [Equals, Between, LessThan, LessThanOrEqualTo, MoreThan,
                MoreThanOrEqualTo, Truthy, Percent, PercentRange]

        return dict((o.name, o) for o in operators)

    @before
    def reload_module(self):
        reload(registry)

    def test_operators_starts_out_with_default_list(self):
        expect(registry.operators).to == self.default_operator_dict

    def test_can_register_operators(self):
        new_operators = dict(operator=sentinel.operator)

        expect(registry.operators).to_not.have_subset(new_operators)
        registry.operators.register(sentinel.operator)
        expect(registry.operators).to.have_subset(new_operators)

    def test_arguments_starts_out_empty(self):
        expect(registry.arguments).to == {}

    def test_operators_to_choices_returns_suitable_tuple(self):
        eq_(
            registry.operators.as_choices,
            [
                (
                    'Comparable', [
                        ('between', 'Between'),
                        ('equals', 'Equal To'),
                        ('before', 'Less Than'),
                        ('less_than_or_equal_to', 'Less Than Or Equal To'),
                        ('more_than', 'More Than'),
                        ('more_than_or_equal_to', 'More Than Or Equal To')
                    ]
                ),
                (
                    'Identity', [
                        ('true', 'True')
                    ]
                ),
                (
                    'Misc', [
                        ('percent_range', 'In The Percentage Range Of'),
                        ('percent', 'Within The Percentage Of')
                    ]
                )
            ]
        )

    def test_arguments_as_choices_returns_suiteable_tuple(self):
        registry.arguments.register(FooArgs.a)
        registry.arguments.register(FooArgs.b)
        registry.arguments.register(BarArgs.a)
        registry.arguments.register(BarArgs.b)

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

    def test_operators_with_arguments_returns_dict_of_name_to_args(self):
        eq_(
            registry.operators.arguments,
            {
                'more_than_or_equal_to': ('lower_limit',),
                'more_than': ('lower_limit',),
                'less_than_or_equal_to': ('upper_limit',),
                'percent': ('percentage',),
                'equals': ('value',),
                'percent_range': ('lower_limit', 'upper_limit'),
                'between': ('lower_limit', 'upper_limit'),
                'true': (),
                'before': ('upper_limit',)
            }
        )
