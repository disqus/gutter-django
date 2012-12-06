from __future__ import absolute_import

from gutter.web import registry

from gutter.client import arguments


class User(arguments.Base):
    name = arguments.String(lambda self: 'Jeff')
    age = arguments.Value(lambda self: 29)
    registered_on = arguments.Boolean(lambda self: True)


class Request(arguments.Base):
    arguments.String('192.168.0.1')


registry.arguments.append(User)
registry.arguments.append(Request)
