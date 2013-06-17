 # coding: utf-8

import unittest2

from django.forms.fields import CharField

from mock import Mock, MagicMock, patch, sentinel, call

from exam import Exam, fixture, patcher, before
from exam.helpers import track

from nose.tools import *

from .fixtures import User  # Also causes the User arguments to be registered
from gutter.django.forms import SwitchForm, ConditionForm, ConditionFormSet, SwitchFormManager
from gutter.client.models import Switch, Condition
from gutter.client.operators.comparable import Equals, MoreThan


class SwitchFormTest(Exam, unittest2.TestCase):

    mock_switch = fixture(Mock, conditions=[1, 2, 3])
    condition_form = patcher('gutter.django.forms.ConditionForm')
    form = fixture(SwitchForm)

    @fixture
    def switch_from_object(self):
        return SwitchForm.from_object(self.mock_switch)

    @patch('gutter.django.forms.ConditionFormSet')
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

    @patch('gutter.django.forms.ConditionFormSet')
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

    def test_from_object_marks_the_name_field_as_readonly(self):
        self.assertTrue(
            self.switch_from_object.fields['name'].widget.attrs['readonly']
        )


class SwitchFormIntegrationTest(Exam, unittest2.TestCase):

    @fixture
    def post_data(self):
        return {
            u'name': u'name',
            u'description': u'description',
            u'state': u'1',
            u'label': u'label',
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
        obj = self.switch_form.to_object
        exp = self.expected_switch

        self.assertEqual(obj.name, exp.name)
        self.assertEqual(obj.label, exp.label)
        self.assertEqual(obj.description, exp.description)
        self.assertEqual(obj.state, exp.state)
        self.assertEqual(obj.compounded, exp.compounded)
        self.assertEqual(obj.concent, exp.concent)

    def test_only_allow_alphanumeric_and_underscore_switch_names(self):
        self.post_data['name'] = 'ಠ_ಠ'
        self.assertFalse(SwitchForm(self.post_data).is_valid())
        self.post_data['name'] = 'i_am_dissapoint'
        self.assertTrue(SwitchForm(self.post_data).is_valid())


class ConditionFormTest(Exam, unittest2.TestCase):

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


class ConditionSetFormTest(Exam, unittest2.TestCase):

    initial = [
        build_initial_row('arg1', 'oper1', **{'1a': '1aval', '1b': '1bval'}),
        build_initial_row('arg2', 'oper2', **{'2a': '2aval'}),
        build_initial_row('arg3', 'oper3', **{'3a': '3aval', '3b': '3bval'})
    ]

    @patcher('gutter.django.forms.operators')
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


class ConditionFormSetIntegrationTest(Exam, unittest2.TestCase):

    post_data = {
        u'form-MAX_NUM_FORMS': u'',
        u'form-TOTAL_FORMS': u'2',
        u'form-INITIAL_FORMS': u'2',

        u'form-0-argument': u'User.name',
        u'form-0-operator': u'equals',
        u'form-0-negative': u'1',
        u'form-0-value': u'Jeff',

        u'form-1-argument': u'User.age',
        u'form-1-operator': u'more_than',
        u'form-1-negative': u'0',
        u'form-1-lower_limit': u'21',
    }

    @fixture
    def expected_condtions(self):
        return [
            Condition(User, 'name', Equals(value='Jeff'), negative=True),
            Condition(User, 'age', MoreThan(lower_limit=21))
        ]

    @fixture
    def valid_formset(self):
        formset = ConditionFormSet(self.post_data)
        self.assertTrue(formset.is_valid())
        return formset

    def test_to_objects_returns_list_on_condition_objects(self):
        self.assertEqual(self.valid_formset.to_objects, self.expected_condtions)


class SwitchFormManagerTest(Exam, unittest2.TestCase):

    @fixture
    def manager(self):
        return SwitchFormManager(MagicMock(), MagicMock())

    gutter_manager = fixture(Mock)

    def test_init_constructs_with_switch_and_conditionset_forms(self):
        manager = SwitchFormManager(sentinel.switch, sentinel.conditionset)
        eq_(manager.switch, sentinel.switch)
        eq_(manager.conditions, sentinel.conditionset)

    @patch('gutter.django.forms.ConditionFormSet')
    @patch('gutter.django.forms.SwitchForm')
    def test_from_post_constructs_switch_and_conditions_then_self(self, s, cfs):
        manager = SwitchFormManager.from_post(sentinel.POST)

        s.assert_called_once_with(sentinel.POST)
        cfs.assert_called_once_with(sentinel.POST)

        eq_(manager.switch, s.return_value)
        eq_(manager.conditions, cfs.return_value)

    def test_is_valid_asks_switch_and_conditions(self):
        self.manager.switch.is_valid.return_value = True
        self.manager.conditions.is_valid.return_value = True
        eq_(self.manager.is_valid(), True)

        self.manager.switch.is_valid.return_value = False
        self.manager.conditions.is_valid.return_value = True
        eq_(self.manager.is_valid(), False)

        self.manager.switch.is_valid.return_value = True
        self.manager.conditions.is_valid.return_value = False
        eq_(self.manager.is_valid(), False)

        self.manager.switch.is_valid.return_value = False
        self.manager.conditions.is_valid.return_value = False
        eq_(self.manager.is_valid(), False)

    def test_save_updates_manager_switch_with_switch_to_object(self):
        self.manager.conditions.__iter__ = [Mock(), Mock()]
        self.manager.save(self.gutter_manager)
        self.gutter_manager.register.assert_called_once_with(
            self.manager.switch.to_object
        )

    def test_save_sets_conditions_on_switch_before_registering(self):
        self.manager.save(self.gutter_manager)
        args, kwargs = self.gutter_manager.register.call_args
        switch = args[0]

        eq_(switch.conditions, self.manager.conditions.to_objects)

    def test_add_to_switch_list_adds_switch_at_name_from_forms(self):
        switches = []
        self.manager.add_to_switch_list(switches)
        eq_(switches[0], self.manager.switch)
        eq_(switches[0].conditions, self.manager.conditions)

    def test_delete_unregisters_switch_with_manager(self):
        self.manager.delete(self.gutter_manager)
        self.gutter_manager.unregister.assert_called_once_with(
            self.manager.switch.data['name']
        )
