from unittest import TestCase

from anompy.detector.base import BaseDetector


class BaseDetectorTestCase(TestCase):

    def test(self):
        th = 5.
        detector = BaseDetector(1, threshold=th)

        observed_series = list(range(2, 11))
        forecasted_series = detector.detect(observed_series)

        self.assertEqual(len(observed_series), len(forecasted_series))

        for observed, (forecasted, anomaly) in zip(observed_series, forecasted_series):
            self.assertEqual(forecasted, observed - 1)

            if (observed - 1) > th:
                self.assertTrue(anomaly)
            else:
                self.assertFalse(anomaly)
