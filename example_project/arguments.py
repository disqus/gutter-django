from gutter.client.arguments import Container


class User(Container):

    def name(self):
        return 'Jeff'

    def age(self):
        return 28


class Request(Container):

    def ip(self):
        return '192.168.0.1'
