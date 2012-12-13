from gutter.web import registry
from gutter.client import arguments


class User:
    name = arguments.String(lambda self: self.input.name)
    age = arguments.Value(lambda self: self.input.age)


registry.arguments.append(User.age)
registry.arguments.append(User.name)
