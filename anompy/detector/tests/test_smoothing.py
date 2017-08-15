from unittest import TestCase

from anompy.detector.smoothing import ExponentialSmoothing, DoubleExponentialSmoothing


class ExponentialSmoothingTestCase(TestCase):

    def test_single(self):
        detector = ExponentialSmoothing(alpha=.1)

        series = [3, 10, 12, 13, 12, 10, 12]
        expected = [3, 3.7, 4.53, 5.377, 6.0393, 6.43537, 6.991833]
        eps = 1e-6

        for i in range(len(series)):
            anomaly = detector.observe(series[i])
            self.assertTrue(anomaly)
            self.assertAlmostEqual(detector.forecast(), expected[i], delta=eps)

    def test_double(self):
        detector = DoubleExponentialSmoothing(alpha=.9, beta=.9)

        series = [3, 10, 12, 13, 12, 10, 12]
        expected = [3, 17.0, 15.45, 14.210500000000001, 11.396044999999999, 8.183803049999998, 12.753698384500002, 13.889016464000003]
        eps = 1e-6

        for i in range(len(series)):
            anomaly = detector.observe(series[i])
            if i < 2:
                continue

            self.assertTrue(anomaly)
            self.assertAlmostEqual(detector.forecast(), expected[i], delta=eps)
