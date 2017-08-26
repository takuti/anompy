from unittest import TestCase

from anompy.detector.average import AverageDetector


class AverageDetectorTestCase(TestCase):

    def test_simple_average(self):
        detector = AverageDetector(1)

        observed_series = list(range(2, 11))
        expected_series = detector.detect(observed_series)

        self.assertEqual(len(observed_series), len(expected_series))

        avg_last = sum_observed = 1.

        for observed, (expected, anomaly) in zip(observed_series, expected_series):
            self.assertAlmostEqual(expected, avg_last, delta=1e-6)
            self.assertTrue(anomaly)

            sum_observed += observed
            avg_last = sum_observed / observed  # `observed` = # of observed data points

    def test_moving_average(self):
        detector = AverageDetector(1, window_size=5)

        observed_series = list(range(2, 6))
        expected_series = detector.detect(observed_series)
        self.assertEqual(len(observed_series), len(expected_series))
        for expected, anomaly in expected_series:
            self.assertTrue(anomaly)

        self.assertAlmostEqual(detector.avg, (1. + sum(observed_series)) / 5, delta=1e-6)

        observed_series = list(range(6, 11))
        expected_series = detector.detect(observed_series)
        self.assertEqual(len(observed_series), len(expected_series))
        for expected, anomaly in expected_series:
            self.assertTrue(anomaly)

        self.assertAlmostEqual(detector.avg, sum(observed_series) / 5, delta=1e-6)

    def test_weighted_moving_average(self):
        detector = AverageDetector(3, window_size=4, weights=[0.4, 0.3, 0.2, 0.1])

        observed_series = [10, 12, 13, 12, 10, 12]
        expected_series = detector.detect(observed_series)

        self.assertEqual(len(observed_series), len(expected_series))

        for expected, anomaly in expected_series:
            self.assertTrue(anomaly)

        self.assertAlmostEqual(detector.avg, 11.5, delta=1e-6)
