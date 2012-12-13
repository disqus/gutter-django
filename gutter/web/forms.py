from django import forms
from django.forms.formsets import formset_factory, BaseFormSet
from django.forms.widgets import Select
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode

from itertools import chain

from gutter.web.registry import operators, arguments

from functools import partial


class OperatorSelectWidget(Select):

    def __init__(self, arguments, *args, **kwargs):
        self.arguments = arguments
        super(OperatorSelectWidget, self).__init__(*args, **kwargs)

    def render_options(self, choices, selected_choices):
        def render_option(option_value, option_label):
            option_value = force_unicode(option_value)
            selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
            return u'<option data-arguments="%s" value="%s"%s>%s</option>' % (
                ','.join(self.arguments[option_value]),
                escape(option_value), selected_html,
                conditional_escape(force_unicode(option_label)))

        # Normalize to strings.
        selected_choices = set([force_unicode(v) for v in selected_choices])
        output = []

        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
                for option in option_label:
                    output.append(render_option(*option))
                output.append(u'</optgroup>')
            else:
                output.append(render_option(option_value, option_label))
        return u'\n'.join(output)


class SwitchForm(forms.Form):

    STATES = {1: 'Disabled', 2: 'Selective', 3: 'Global'}

    name = forms.CharField(max_length=100)
    label = forms.CharField()
    description = forms.CharField()
    state = forms.IntegerField()  # TODO: change to select box

    compounded = forms.BooleanField(required=False)
    concent = forms.BooleanField(required=False)

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

        instance = cls(initial=data)

        condition_dicts = map(ConditionForm.to_dict, switch.conditions)
        instance.conditions = ConditionFormSet(initial=condition_dicts)

        return instance


class ConditionForm(forms.Form):

    NEGATIVE_CHOICES = ((0, 'Is'), (1, 'Is Not'))

    argument = forms.ChoiceField(choices=arguments.as_choices)
    negative = forms.ChoiceField(choices=NEGATIVE_CHOICES)
    operator = forms.ChoiceField(
        choices=operators.as_choices,
        widget=OperatorSelectWidget(operators.arguments)
    )

    @staticmethod
    def to_dict(condition):
        fields = dict(
            argument='.'.join((condition.argument.__name__, condition.attribute)),
            negative=condition.negative,
            operator=condition.operator.name
        )

        fields.update(condition.operator.variables)

        return fields


class BaseConditionFormSet(BaseFormSet):

    def value_at(self, index, field):
        if self.initial:
            return self.initial[index][field]
        else:
            return self.data['form-%s-%s' % (index, field)]

    def add_fields(self, form, index):
        value = partial(self.value_at, index)

        for argument in operators.arguments[value('operator')]:
            form.fields[argument] = forms.CharField(initial=value(argument))

        super(BaseConditionFormSet, self).add_fields(form, index)


ConditionFormSet = formset_factory(
    ConditionForm,
    formset=BaseConditionFormSet,
    extra=0
)
