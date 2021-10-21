import unittest

from bes.auth import BESAuth
from tests.config import settings


class TestBESAuth(unittest.TestCase):

    def setUp(self) -> None:
        print(settings)
        self.auth = BESAuth.oauth2(**settings.to_oauth2config())
        self.auth.oauth2client.fetch_token(**settings.to_oauth2_auth_basic())
        self.auth.initial()

    def tearDown(self) -> None:
        self.auth.oauth2client.close()

    def test_initial(self):
        pass
