from __future__ import absolute_import

from gutter.web import registry

from gutter.client.arguments import Base


class User(Base):

    def name(self):
        return 'Jeff'

    def age(self):
        return 28


class Request(Base):

    def ip(self):
        return '192.168.0.1'


registry.arguments.append(User)
registry.arguments.append(Request)
