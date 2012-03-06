import settings

from gargoyle.client.singleton import gargoyle
from gargoyle.client.models import Switch, Condition
from gargoyle.client.operators.identity import Truthy

switch = Switch('cool_feature', label='A cool feature')
condition = Condition(True, Truthy())
switch.conditions.append(condition)
gargoyle.register(switch)