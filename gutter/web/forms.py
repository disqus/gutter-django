from django import forms
from django.forms.formsets import formset_factory

# from itertools import groupby

from gutter.web.registry import operators, arguments


ARGUMENT_CHOICES = [
    (container.__name__, [(k, k) for (k, v) in container.arguments.items()])
    for container in arguments
]

grouped_operators = {}
for operator in operators:
    grouped_operators.setdefault(operator.group, [])
    grouped_operators[operator.group].append(
        (operator.label, operator.preposition)
    )


GROUPED_OPERATORS = grouped_operators.items()


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

    arguments = forms.ChoiceField(choices=ARGUMENT_CHOICES)
    negative = forms.ChoiceField(choices=NEGATIVE_CHOICES)
    operators = forms.ChoiceField(choices=grouped_operators.items())
    # description = forms.CharField()

    @staticmethod
    def to_dict(condition):
        return {}


ConditionFormSet = formset_factory(ConditionForm)
