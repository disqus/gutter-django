from gutter.client.operators.comparable import *  # noqa
from gutter.client.operators.identity import *  # noqa
from gutter.client.operators.misc import *  # noqa
from gutter.client.operators.string import *  # noqa

from itertools import groupby

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

    @property
    def as_choices(self):
        sorted_strings = sorted(map(str, self.values()))
        extract_classname = lambda a: a.split('.')[0]

        grouped = groupby(sorted_strings, extract_classname)

        groups = {}
        for name, args in grouped:
            groups.setdefault(name, [])
            groups[name].extend((a, a) for a in args)

        return groups.items()

    def register(self, argument):
        self[str(argument)] = argument


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
