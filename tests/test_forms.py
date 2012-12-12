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


class ConditionSetFormTest(Exam, unittest.TestCase):

    initial = [
        dict(argument='arg1', negative=False, operator='oper1'),
        dict(argument='arg2', negative=False, operator='oper2'),
        dict(argument='arg3', negative=False, operator='oper3')
    ]

    @patcher('gutter.web.forms.operators')
    def known_operator_arguments(self):
        operators = Mock()
        operators.arguments = dict(
            oper1=('1a', '1b'),
            oper2=('2a',),
            oper3=('3a', '3b', '3c'),
        )
        return operators

    @fixture
    def formset(self):
        return ConditionFormSet(initial=self.initial)

    def assertIsCharField(self, forms_index, argument_name):
        self.assertIsInstance(
            self.formset.forms[forms_index].fields[argument_name],
            CharField
        )

    def test_adds_a_field_per_argument_of_operator(self):
        self.assertIsCharField(0, '1a')
        self.assertIsCharField(0, '1b')
        self.assertIsCharField(1, '2a')
        self.assertIsCharField(2, '3a')
        self.assertIsCharField(2, '3b')
        self.assertIsCharField(2, '3c')
