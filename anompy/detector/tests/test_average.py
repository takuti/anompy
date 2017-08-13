from unittest import TestCase

from anompy.detector.average import AverageDetector


class AverageDetectorTestCase(TestCase):

    def test_simple_average(self):
        detector = AverageDetector()
        s = 0.

        for x in range(1, 11):
            anomaly = detector.observe(x)
            self.assertTrue(anomaly)
            s += x
            self.assertAlmostEqual(detector.forecast(), s / x, delta=1e-6)

    def test_moving_average(self):
        detector = AverageDetector(window_size=5)

        for x in range(1, 6):
            anomaly = detector.observe(x)
            self.assertTrue(anomaly)
        self.assertAlmostEqual(detector.forecast(), sum(range(1, 6)) / 5, delta=1e-6)

        for x in range(6, 11):
            anomaly = detector.observe(x)
            self.assertTrue(anomaly)
        self.assertAlmostEqual(detector.forecast(), sum(range(6, 11)) / 5, delta=1e-6)

    def test_weighted_moving_average(self):
        detector = AverageDetector(window_size=4, weights=[0.1, 0.2, 0.3, 0.4])

        for x in [3, 10, 12, 13, 12, 10, 12]:
            anomaly = detector.observe(x)
            self.assertTrue(anomaly)
        self.assertAlmostEqual(detector.forecast(), 11.5, delta=1e-6)
