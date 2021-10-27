import unittest
from datetime import date

from bes.builder.query import Dimension, Lookups, GroupBy, Filters, Query


class TestDimension(unittest.TestCase):

    def test_default_initial(self):
        dimension = Dimension(dimension="dimension")

        lookups = Lookups(include=[1, 2], exclude=[2])
        empty_lookups = Lookups()

        dimension_with_lookups = Dimension(dimension="dimension2", lookups=lookups)
        dimension_with_empty_lookups = Dimension(dimension="dimension3", lookups=empty_lookups)

        group_by = GroupBy([dimension, dimension_with_empty_lookups])
        empty_group_by = GroupBy()

        filters = Filters([dimension_with_lookups])
        empty_filters = Filters()

        query = Query(filters=filters)
        empty_query = Query()

    def test_lookups_with_date(self):
        lookups = Lookups(include=[date(2020, 1, 1), date(2020, 1, 2)])

        self.assertEqual(
            lookups.json(include={"include"}),
            '{"include": ["2020-01-01", "2020-01-02"]}'
        )
