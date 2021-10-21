import unittest

from bes.builder.query import Dimension, Lookups, GroupBy, Filters, Query


class TestDimension(unittest.TestCase):

    def test_default_initial(self):
        self.dimension = Dimension(dimension="dimension")

        self.lookups = Lookups(include=[1, 2], exclude=[2])
        self.empty_lookups = Lookups()

        self.dimension_with_lookups = Dimension(dimension="dimension2", lookups=self.lookups)
        self.dimension_with_empty_lookups = Dimension(dimension="dimension3", lookups=self.empty_lookups)

        self.group_by = GroupBy([self.dimension, self.dimension_with_empty_lookups])
        self.empty_group_by = GroupBy()

        self.filters = Filters([self.dimension_with_lookups])
        self.empty_filters = Filters()

        self.query = Query(filters=self.filters)
        self.empty_query = Query()
