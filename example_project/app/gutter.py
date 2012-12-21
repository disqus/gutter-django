from __future__ import absolute_import

from gutter.django import registry

from gutter.client import arguments


class User(arguments.Container):
    name = arguments.String(lambda self: 'Jeff')
    age = arguments.Value(lambda self: 29)
    registered_on = arguments.Boolean(lambda self: True)


class Request(arguments.Container):
    ip = arguments.String('192.168.0.1')


registry.arguments.register(User.name)
registry.arguments.register(User.age)
registry.arguments.register(User.registered_on)
registry.arguments.register(Request.ip)
