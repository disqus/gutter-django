from django import forms
from django.forms.formsets import formset_factory, BaseFormSet

from gutter.web.registry import operators, arguments


class SwitchForm(forms.Form):

    STATES = {1: 'Disabled', 2: 'Selective', 3: 'Global'}

    name = forms.CharField(max_length=100)
    label = forms.CharField()
    description = forms.CharField()
    state = forms.ChoiceField(choices=STATES.items())

    compounded = forms.BooleanField(required=False)
    concenting = forms.BooleanField(required=False)

    def __init__(self, conditions, *args, **kwargs):
        super(SwitchForm, self).__init__(*args, **kwargs)
        self.conditions = ConditionFormSet(
            conditions,
            initial=map(ConditionForm.to_dict, conditions)
        )

    @classmethod
    def from_object(cls, switch):
        data = dict(
            label=switch.label,
            name=switch.name,
            description=switch.description,
            state=switch.state,
            compounded=switch.compounded,
            concent=switch.concent
        )

        return cls(switch.conditions, data)


class ConditionForm(forms.Form):

    NEGATIVE_CHOICES = ((0, 'Is'), (1, 'Is Not'))

    argument = forms.ChoiceField(choices=arguments.as_choices)
    negative = forms.ChoiceField(choices=NEGATIVE_CHOICES)
    operator = forms.ChoiceField(choices=operators.as_choices)

    @staticmethod
    def to_dict(condition):
        return dict(
            argument='.'.join((condition.argument.__name__, condition.attribute)),
            negative=condition.negative,
            operator=condition.operator.name
        )


class BaseConditionFormSet(BaseFormSet):

    def __init__(self, conditions=None, *args, **kwargs):
        self.conditions = conditions
        super(BaseConditionFormSet, self).__init__(*args, **kwargs)

    def add_fields(self, form, index):
        try:
            condition_obj = self.conditions[index]
        except IndexError:
            return  # Assume it's the extra input
        else:
            for name, value in condition_obj.operator.arguments.items():
                form.fields[name] = forms.CharField(initial=value)

        super(BaseConditionFormSet, self).add_fields(form, index)


ConditionFormSet = formset_factory(ConditionForm, formset=BaseConditionFormSet)
