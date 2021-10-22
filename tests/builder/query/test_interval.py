import unittest

from bes.builder.query import DateRange, PrevDateRange


class TestInterval(unittest.TestCase):

    def test_default_initial(self):
        date_range = DateRange.default()
        prev_date_range = PrevDateRange.default()
