import unittest

from bes.builder.query.metric import Metric, Aggregate


class TestMetric(unittest.TestCase):

    def test_default_initial(self):
        self.metric = Metric(metric="metric")

        self.aggregate = Aggregate([self.metric])
        self.empty_aggregate = Aggregate()
