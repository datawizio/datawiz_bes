import unittest

from bes.auth import BESAuth
from bes.builder import BESBuilder, BuilderQuery
from bes.builder.query import Metric, Aggregate, Dimension, GroupBy, Lookups, Filters
from tests.config import settings


class TestBESBuilder(unittest.TestCase):

    def setUp(self) -> None:
        self.auth = BESAuth.oauth2(**settings.to_oauth2config())
        self.auth.oauth2client.fetch_token(**settings.to_oauth2_auth_basic())
        self.auth.initial()

    @staticmethod
    def get_builder_query() -> BuilderQuery:
        return BuilderQuery(
            aggregate=Aggregate([Metric(metric="turnover")]),
            group_by=GroupBy([Dimension(dimension="shop")]),
            filters=Filters([Dimension(dimension="category", lookups=Lookups(include=[6779]))])
        )

    def test_builder_default(self):
        query = self.get_builder_query()
        builder = BESBuilder(query=query, auth=self.auth)
        data = builder.fetch_all()
        self.assertEqual("results" in data, True)
