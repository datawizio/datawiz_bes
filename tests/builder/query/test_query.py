import unittest

from bes.builder.query import BuilderQuery


class TestBuilderQuery(unittest.TestCase):

    def test_default_initial(self):
        self.builder_query = BuilderQuery()
