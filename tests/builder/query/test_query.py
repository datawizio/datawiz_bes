import unittest

from bes.builder.query import BuilderQuery


class TestBuilderQuery(unittest.TestCase):

    def setUp(self) -> None:
        self.builder_query = BuilderQuery()

    def test_json_dumps(self):
        self.builder_query.to_json()

    def test_model_dump_and_dump_json_no_errors(self):
        BuilderQuery().model_dump()
        BuilderQuery().model_dump_json()
