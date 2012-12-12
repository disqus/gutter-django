import unittest

from django.forms.fields import CharField

from mock import Mock, MagicMock, patch

from exam import Exam, fixture, patcher

from nose.tools import *

from gutter.web.forms import SwitchForm, ConditionForm, ConditionFormSet


class SwitchFormTest(Exam, unittest.TestCase):

    switch = fixture(Mock, conditions=[1, 2, 3])
    condition_form = patcher('gutter.web.forms.ConditionForm')

    @fixture
    def switch_from_object(self):
        return SwitchForm.from_object(self.switch)

    @patch('gutter.web.forms.ConditionFormSet')
    def test_from_object_returns_dict_of_properties(self, _):
        eq_(
            self.switch_from_object.initial,
            dict(
                label=self.switch.label,
                name=self.switch.name,
                description=self.switch.description,
                state=self.switch.state,
                compounded=self.switch.compounded,
                concent=self.switch.concent,
            )
        )

    @patch('gutter.web.forms.ConditionFormSet')
    def test_from_object_sets_conditions_as_form_set(self, ConditionFormSet):
        eq_(
            self.switch_from_object.conditions,
            ConditionFormSet.return_value
        )

        # Called with a map() over ConditionForm.to_dict
        expected = [self.condition_form.to_dict.return_value] * 3
        ConditionFormSet.assert_called_once_with(initial=expected)

        # Assert that the calls it did receive are correct
        self.condition_form.to_dict.assert_any_call(1)
        self.condition_form.to_dict.assert_any_call(2)
        self.condition_form.to_dict.assert_any_call(3)


class ConditionFormTest(Exam, unittest.TestCase):

    @fixture
    def condition(self):
        return MagicMock(**{'argument.__name__': 'name', 'attribute': 'attr'})

    def test_to_dict_extracts_out_relevant_parts_of_condition(self):
        eq_(
            ConditionForm.to_dict(self.condition),
            dict(
                argument='name.attr',
                negative=self.condition.negative,
                operator=self.condition.operator.name
            )
        )


def build_initial_row(argument, operator, **kwargs):
    results = dict(argument=argument, negative=False, operator=operator)
    results.update(kwargs)
    return results


class ConditionSetFormTest(Exam, unittest.TestCase):

    initial = [
        build_initial_row('arg1', 'oper1', **{'1a': '1aval', '1b': '1bval'}),
        build_initial_row('arg2', 'oper2', **{'2a': '2aval'}),
        build_initial_row('arg3', 'oper3', **{'3a': '3aval', '3b': '3bval'})
    ]

    @patcher('gutter.web.forms.operators')
    def known_operator_arguments(self):
        operators = Mock()
        operators.arguments = dict(
            oper1=('1a', '1b'),
            oper2=('2a',),
            oper3=('3a', '3b'),
        )
        return operators

    @fixture
    def formset(self):
        return ConditionFormSet(initial=self.initial)

    def field_at(self, forms_index, argument_name):
        return self.formset.forms[forms_index].fields[argument_name]

    def assertIsCharField(self, forms_index, argument_name):
        self.assertIsInstance(
            self.field_at(forms_index, argument_name),
            CharField
        )

    def assertInitialValue(self, forms_index, argument_name, initial):
        self.assertEquals(
            self.formset.forms[forms_index].fields[argument_name].initial,
            initial
        )

    def test_adds_a_field_per_argument_of_operator(self):
        self.assertIsCharField(0, '1a')
        self.assertIsCharField(0, '1b')
        self.assertIsCharField(1, '2a')
        self.assertIsCharField(2, '3a')
        self.assertIsCharField(2, '3b')

    def test_sets_the_initial_value_for_each_field(self):
        self.assertEquals(self.field_at(0, '1a').initial, '1aval')
        self.assertEquals(self.field_at(0, '1b').initial, '1bval')
        self.assertEquals(self.field_at(1, '2a').initial, '2aval')
        self.assertEquals(self.field_at(2, '3a').initial, '3aval')
        self.assertEquals(self.field_at(2, '3b').initial, '3bval')
