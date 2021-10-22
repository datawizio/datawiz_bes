import unittest

from bes.builder.query.metric import Metric, Aggregate


class TestMetric(unittest.TestCase):

    def test_default_initial(self):
        metric = Metric(metric="metric")

        aggregate = Aggregate([metric])
        empty_aggregate = Aggregate()
