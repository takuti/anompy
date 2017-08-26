from unittest import TestCase

from anompy.detector.base import BaseDetector


class BaseDetectorTestCase(TestCase):

    def test(self):
        th = 5.
        detector = BaseDetector(1, threshold=th)

        observed_series = list(range(2, 11))
        expected_series = detector.detect(observed_series)

        self.assertEqual(len(observed_series), len(expected_series))

        for observed, (expected, anomaly) in zip(observed_series, expected_series):
            self.assertEqual(expected, observed - 1)

            if (observed - 1) > th:
                self.assertTrue(anomaly)
            else:
                self.assertFalse(anomaly)
