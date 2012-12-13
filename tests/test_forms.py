import unittest

from django.forms.fields import CharField

from mock import Mock, MagicMock, patch

from exam import Exam, fixture, patcher, before

from nose.tools import *

from .fixtures import User  # Also causes the User arguments to be registered
from gutter.web.forms import SwitchForm, ConditionForm, ConditionFormSet
from gutter.client.models import Switch, Condition
from gutter.client.operators.comparable import Equals, MoreThan


class SwitchFormTest(Exam, unittest.TestCase):

    mock_switch = fixture(Mock, conditions=[1, 2, 3])
    condition_form = patcher('gutter.web.forms.ConditionForm')

    @fixture
    def switch_from_object(self):
        return SwitchForm.from_object(self.mock_switch)

    @patch('gutter.web.forms.ConditionFormSet')
    def test_from_object_returns_dict_of_properties(self, _):
        eq_(
            self.switch_from_object.initial,
            dict(
                label=self.mock_switch.label,
                name=self.mock_switch.name,
                description=self.mock_switch.description,
                state=self.mock_switch.state,
                compounded=self.mock_switch.compounded,
                concent=self.mock_switch.concent,
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


class SwitchFormIntegrationTest(Exam, unittest.TestCase):

    post_data = {
        u'name': u'name',
        u'description': u'description',
        u'state': u'1',
        u'label': u'label',
        u'compounded': u'0',
        u'concent': u'0',
    }

    @fixture
    def switch_form(self):
        return SwitchForm(self.post_data)

    @fixture
    def expected_switch(self):
        return Switch(
            name='name',
            label='label',
            description='description',
            state=1,
            compounded=False,
            concent=False,
        )

    @before
    def assert_is_valid(self):
        self.assertTrue(self.switch_form.is_valid())

    def test_to_object_returns_object_from_form(self):
        self.assertEqual(self.switch_form.to_object, self.expected_switch)


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


class ConditionFormSetIntegrationTest(Exam, unittest.TestCase):

    post_data = {
        u'form-MAX_NUM_FORMS': u'',
        u'form-TOTAL_FORMS': u'2',
        u'form-INITIAL_FORMS': u'2',

        u'form-0-argument': u'User.name',
        u'form-0-operator': u'equals',
        u'form-0-negative': u'0',
        u'form-0-value': u'Jeff',

        u'form-1-argument': u'User.age',
        u'form-1-operator': u'more_than',
        u'form-1-negative': u'0',
        u'form-1-lower_limit': u'21',
    }

    @fixture
    def expected_condtions(self):
        return (
            Condition(User, 'name', Equals(value='Jeff')),
            Condition(User, 'age', MoreThan(lower_limit=21))
        )

    def test_to_objects_returns_list_on_condition_objects(self):
        formset = ConditionFormSet(self.post_data)
        self.assertTrue(formset.is_valid())
        self.assertEquals(formset.to_objects, self.expected_condtions)
