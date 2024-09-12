import os

from unittest import TestCase


class MobifyTestCase(TestCase):

    def get_dir(self) -> str:
        return os.path.dirname(os.path.abspath(__file__))

    def get_fixture(self, name) -> str:
        with open(f'{self.get_dir()}/fixtures/{name}', 'rt') as fixture:
            return fixture.read()
