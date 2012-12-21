from gutter.django import registry
from gutter.client import arguments


class User:
    name = arguments.String(lambda self: self.input.name)
    age = arguments.Integer(lambda self: self.input.age)


registry.arguments.register(User.age)
registry.arguments.register(User.name)
