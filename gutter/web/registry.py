from gutter.client.operators.comparable import *
from gutter.client.operators.identity import *
from gutter.client.operators.misc import *

from itertools import groupby


class OperatorsList(list):

    @property
    def as_choices(self):
        groups = {}

        for operator in operators:
            key = operator.group.title()
            pair = (operator.name, operator.preposition.title())

            groups.setdefault(key, [])
            groups[key].append(pair)

        return groups.items()


class ArgumentsList(list):

    @property
    def as_choices(self):
        groups = {}
        grouped = groupby(map(str, self), lambda a: a.split('.')[0])

        for name, arguments in grouped:
            groups.setdefault(name, [])
            groups[name].extend((a, a) for a in arguments)

        return groups.items()


operators = OperatorsList((
    Equals,
    Between,
    LessThan,
    LessThanOrEqualTo,
    MoreThan,
    MoreThanOrEqualTo,
    Truthy,
    Percent,
    PercentRange
))

arguments = ArgumentsList()
