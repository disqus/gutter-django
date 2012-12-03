from gutter.client.operators.comparable import *
from gutter.client.operators.identity import *
from gutter.client.operators.misc import *

operators = list((
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

arguments = []
