from gutter.client.operators.comparable import *  # noqa
from gutter.client.operators.identity import *  # noqa
from gutter.client.operators.misc import *  # noqa
from gutter.client.operators.string import *  # noqa

import bisect

from operator import attrgetter, itemgetter


class OperatorsDict(dict):

    def __init__(self, *ops):
        for o in ops:
            self.register(o)

    def register(self, operator):
        self[operator.name] = operator

    @property
    def as_choices(self):
        groups = {}

        for operator in sorted(self.values(), key=attrgetter('preposition')):
            key = operator.group.title()
            pair = (operator.name, operator.preposition.title())

            groups.setdefault(key, [])
            groups[key].append(pair)

        return sorted(groups.items(), key=itemgetter(0))

    @property
    def arguments(self):
        return dict((name, op.arguments) for name, op in self.items())


class ArgumentsDict(dict):
    """
    Moved all sorts from as_choices to register method to avoid recalculation on every condition form render
    It's a possibility to have hundreds of them on the page
    """

    __choices = []
    __args = {}

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
