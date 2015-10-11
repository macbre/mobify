import os

from unittest import TestCase


class MobifyTestCase(TestCase):

    @property
    def __dir__(self):
        return os.path.dirname(os.path.abspath(__file__))

    def get_fixture(self, name):
        with open(self.__dir__ + '/fixtures/{}'.format(name)) as fixture:
            return fixture.read()
