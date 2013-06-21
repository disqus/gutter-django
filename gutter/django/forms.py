from django import forms
from django.core.validators import RegexValidator
from django.forms.formsets import formset_factory, BaseFormSet
from django.forms.widgets import Select, Textarea
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode

from itertools import chain

from gutter.django.registry import operators, arguments
from gutter.client.models import Switch, Condition

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

    STATES = {1: 'Disabled', 2: 'Selective', 3: 'Global'}.items()
    SWITCH_NAME_REGEX_VALIDATOR = RegexValidator(
        regex=r'^[\w_:]+$',
        message='Must only be alphanumeric, underscore, and colon characters.'
    )

    name = forms.CharField(max_length=100)
    label = forms.CharField(required=False)
    description = forms.CharField(widget=Textarea(), required=False)
    state = forms.IntegerField(widget=Select(choices=STATES))

    compounded = forms.BooleanField(required=False)
    concent = forms.BooleanField(required=False)

    delete = forms.BooleanField(required=False)

    name.validators.append(SWITCH_NAME_REGEX_VALIDATOR)

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
        instance.fields['name'].widget.attrs['readonly'] = True

        return instance

    def field(self, key):
        return self.data.get(key, None) or self.initial[key]

    @property
    def to_object(self):
        switch = Switch(
            name=self.cleaned_data['name'],
            label=self.cleaned_data['label'],
            description=self.cleaned_data['description'],
            state=self.cleaned_data['state'],
            compounded=self.cleaned_data['compounded'],
            concent=self.cleaned_data['concent'],
        )

        return switch


class ConditionForm(forms.Form):

    negative_widget = Select(choices=((False, 'Is'), (True, 'Is Not')))

    argument = forms.ChoiceField(choices=arguments.as_choices)
    negative = forms.BooleanField(widget=negative_widget, required=False)
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

    @property
    def to_objects(self):
        return map(self.__make_condition, self.forms)

    def __make_condition(self, form):
        data = form.cleaned_data.copy()

        # Extract out the values from the POST data.  These are all strings at
        # this point
        operator_str = data.pop('operator')
        negative_str = data.pop('negative')
        argument_str = data.pop('argument')

        # Operators in the registry are the types (classes), so extract that out
        # and we will construct it from the remaining data, which are the
        # arguments for the operator
        operator_type = operators[operator_str]

        # Arguments are a Class property, so just a simple fetch from the
        # arguments dict will retreive it
        argument = arguments[argument_str]

        # The remaining variables in the data are the arguments to the operator,
        # but they need to be cast by the argument to their right type
        caster = argument.variable.to_python
        data = dict((k, caster(v)) for k, v in data.items())

        return Condition(
            argument=argument.owner,
            attribute=argument.name,
            operator=operator_type(**data),
            negative=bool(int(negative_str))
        )

    def value_at(self, index, field):
        if self.initial:
            return self.initial[index][field]
        elif index is not None:
            return self.data['form-%s-%s' % (index, field)]

    def add_fields(self, form, index):
        value = partial(self.value_at, index)

        for argument in operators.arguments.get(value('operator'), []):
            form.fields[argument] = forms.CharField(initial=value(argument))

        super(BaseConditionFormSet, self).add_fields(form, index)


ConditionFormSet = formset_factory(
    ConditionForm,
    formset=BaseConditionFormSet,
    extra=0
)


class SwitchFormManager(object):

    def __init__(self, switch, condition_set):
        self.switch = switch
        self.conditions = condition_set

    @classmethod
    def from_post(cls, post_data):
        return cls(SwitchForm(post_data), ConditionFormSet(post_data))

    def is_valid(self):
        return self.switch.is_valid() and self.conditions.is_valid()

    def save(self, gutter_manager):
        switch = self.switch.to_object
        switch.conditions = self.conditions.to_objects
        gutter_manager.register(switch)

    def add_to_switch_list(self, switches):
        self.switch.conditions = self.conditions
        switches.insert(0, self.switch)

    def delete(self, gutter_manager):
        gutter_manager.unregister(self.switch.data['name'])
