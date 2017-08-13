from unittest import TestCase

from anompy.detector.smoothing import ExponentialSmoothing


class ExponentialSmoothingTestCase(TestCase):

    def test(self):
        detector = ExponentialSmoothing(alpha=.1)

        series = [3, 10, 12, 13, 12, 10, 12]
        expected = [3, 3.7, 4.53, 5.377, 6.0393, 6.43537, 6.991833]
        eps = 1e-6

        for i in range(len(series)):
            anomaly = detector.observe(series[i])
            self.assertTrue(anomaly)
            self.assertAlmostEqual(detector.forecast(), expected[i], delta=eps)
