import unittest

from bes.builder.query import DateRange, PrevDateRange


class TestInterval(unittest.TestCase):

    def test_default_initial(self):
        self.date_range = DateRange.default()
        self.prev_date_range = PrevDateRange.default()
