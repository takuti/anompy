from unittest import TestCase

from anompy.detector.average import AverageDetector


class AverageDetectorTestCase(TestCase):

    def test_simple_average(self):
        detector = AverageDetector(1)

        observed_series = list(range(2, 11))
        forecasted_series = detector.detect(observed_series)

        self.assertEqual(len(observed_series), len(forecasted_series))

        average_last = sum_observed = 1.

        for observed, (forecasted, anomaly) in zip(observed_series, forecasted_series):
            self.assertAlmostEqual(forecasted, average_last, delta=1e-6)
            self.assertTrue(anomaly)

            sum_observed += observed
            average_last = sum_observed / observed  # `observed` = # of observed data points

    def test_moving_average(self):
        detector = AverageDetector(1, window_size=5)

        observed_series = list(range(2, 6))
        forecasted_series = detector.detect(observed_series)
        self.assertEqual(len(observed_series), len(forecasted_series))
        for forecasted, anomaly in forecasted_series:
            self.assertTrue(anomaly)

        self.assertAlmostEqual(detector.average, (1. + sum(observed_series)) / 5, delta=1e-6)

        observed_series = list(range(6, 11))
        forecasted_series = detector.detect(observed_series)
        self.assertEqual(len(observed_series), len(forecasted_series))
        for forecasted, anomaly in forecasted_series:
            self.assertTrue(anomaly)

        self.assertAlmostEqual(detector.average, sum(observed_series) / 5, delta=1e-6)

    def test_weighted_moving_average(self):
        detector = AverageDetector(3, window_size=4, weights=[0.4, 0.3, 0.2, 0.1])

        observed_series = [10, 12, 13, 12, 10, 12]
        forecasted_series = detector.detect(observed_series)

        self.assertEqual(len(observed_series), len(forecasted_series))

        for forecasted, anomaly in forecasted_series:
            self.assertTrue(anomaly)

        self.assertAlmostEqual(detector.average, 11.5, delta=1e-6)
