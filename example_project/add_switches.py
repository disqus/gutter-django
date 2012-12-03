import settings

from gutter.client.default import gutter
from gutter.client.models import Switch, Condition
from gutter.client.operators.misc import Percent
from gutter.client.operators.comparable import Equals, MoreThan

from example_project.arguments import User, Request

switch = Switch('cool_feature', label='A cool feature', description='Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.')

condition = Condition(User, 'name', Equals('Jeff'))
switch.conditions.append(condition)

condition = Condition(User, 'age', MoreThan(21))
switch.conditions.append(condition)

gutter.register(switch)

switch = Switch('other_neat_feature', label='A neat additional feature', description='Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.')

condition = Condition(Request, 'ip', Percent(10))
switch.conditions.append(condition)

gutter.register(switch)

for switch in gutter.switches:
    print '+', switch

print type(gutter.storage)