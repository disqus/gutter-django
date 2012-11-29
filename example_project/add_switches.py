import settings

from chimera.client.singleton import chimera
from chimera.client.models import Switch, Condition
from chimera.client.operators.misc import Percent
from chimera.client.operators.comparable import Equals, MoreThan

from example_project.arguments import User, Request

switch = Switch('cool_feature', label='A cool feature', description='Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.')

condition = Condition(User.name, Equals('Jeff'))
switch.conditions.append(condition)

condition = Condition(User.age, MoreThan(21))
switch.conditions.append(condition)

chimera.register(switch)

switch = Switch('other_neat_feature', label='A neat additional feature', description='Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.')

condition = Condition(Request.ip, Percent(10))
switch.conditions.append(condition)

chimera.register(switch)
