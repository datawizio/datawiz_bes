import unittest

from bes.builder.query import BuilderQuery


class TestBuilderQuery(unittest.TestCase):

    def setUp(self) -> None:
        self.builder_query = BuilderQuery()

    def test_json_dumps(self):
        self.builder_query.to_json()
