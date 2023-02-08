from gutter.client.operators.comparable import *  # noqa
from gutter.client.operators.identity import *  # noqa
from gutter.client.operators.misc import *  # noqa
from gutter.client.operators.string import *  # noqa

import bisect


class OperatorsDict(dict):
    """
    Moved all sorts from as_choices to register method to avoid recalculation on every condition form render
    It's a possibility to have hundreds of them on the page
    """

    def __init__(self, *ops):
        self.__choices = []
        self.__groups = {}
        self.__args = {}

        for o in ops:
            self.register(o)

    def register(self, operator):
        self[operator.name] = operator

        self.__args[operator.name] = getattr(operator, 'arguments', None)

        if hasattr(operator, 'group'):
            key = operator.group.title()
            self.__groups.setdefault(key, (key, []))
            pair = (operator.name, operator.preposition.title())
            self.__groups[key][1].append(pair)
            self.__groups[key] = (key, sorted(self.__groups[key][1], key=lambda x: x[1]))

            self.__choices = sorted(self.__groups.values(), key=lambda x: x[0])

    @property
    def as_choices(self):
        return self.__choices

    @property
    def arguments(self):
        return self.__args


class ArgumentsDict(dict):
    """
    Moved all sorts from as_choices to register method to avoid recalculation on every condition form render
    It's a possibility to have hundreds of them on the page
    """

    def __init__(self, *args, **kwargs):
        self.__choices = []
        self.__args = {}

        super().__init__(*args, **kwargs)

    @property
    def as_choices(self):
        return self.__choices

    def register(self, argument):
        str_argument = str(argument)
        self[str_argument] = argument

        classname, arg = str_argument.split('.')
        self.__args.setdefault(classname, (classname, []))
        bisect.insort_left(self.__args[classname][1], (str_argument, str_argument))

        self.__choices = sorted(self.__args.values(), key=lambda x: x[0])


operators = OperatorsDict(
    Equals,
    Between,
    LessThan,
    LessThanOrEqualTo,
    MoreThan,
    MoreThanOrEqualTo,
    EqualsStripIgnoreCase,
    Truthy,
    Percent,
    PercentRange
)

arguments = ArgumentsDict()
