from __future__ import absolute_import

from gutter.web import registry

from gutter.client import arguments


class User(arguments.Container):
    name = arguments.String(lambda self: 'Jeff')
    age = arguments.Value(lambda self: 29)
    registered_on = arguments.Boolean(lambda self: True)


class Request(arguments.Container):
    ip = arguments.String('192.168.0.1')


registry.arguments.append(User.name)
registry.arguments.append(User.age)
registry.arguments.append(User.registered_on)
registry.arguments.append(Request.ip)
