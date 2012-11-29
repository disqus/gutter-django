from chimera.client.inputs import Base


class User(Base):

    def name(self):
        return 'Jeff'

    def age(self):
        return 28


class Request(Base):

    def ip(self):
        return '192.168.0.1'
