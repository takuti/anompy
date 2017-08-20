from unittest import TestCase

from anompy.detector.smoothing import ExponentialSmoothing, DoubleExponentialSmoothing


class ExponentialSmoothingTestCase(TestCase):

    def setUp(self):
        self.series = [3, 10, 12, 13, 12, 10, 12]
        self.eps = 1e-6

    def test_single(self):
        detector = ExponentialSmoothing(alpha=.1)

        expected = [3, 3.7, 4.53, 5.377, 6.0393, 6.43537, 6.991833]

        for i in range(len(self.series)):
            anomaly = detector.observe(self.series[i])
            self.assertTrue(anomaly)
            self.assertAlmostEqual(detector.forecast(), expected[i], delta=self.eps)

    def test_double(self):
        detector = DoubleExponentialSmoothing(alpha=.9, beta=.9)

        expected = [3, 17.0, 15.45, 14.210500000000001, 11.396044999999999, 8.183803049999998, 12.753698384500002, 13.889016464000003]

        for i in range(len(self.series)):
            anomaly = detector.observe(self.series[i])
            self.assertTrue(anomaly)
            self.assertAlmostEqual(detector.forecast(), expected[i], delta=self.eps)
