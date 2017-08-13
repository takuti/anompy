from unittest import TestCase

from anompy.detector.base import BaseDetector


class BaseDetectorTestCase(TestCase):

    def test(self):
        th = 5.
        detector = BaseDetector(threshold=th)

        for x in range(1, 11):
            anomaly = detector.observe(x)
            if x > th:
                self.assertTrue(anomaly)
            else:
                self.assertFalse(anomaly)
            self.assertEqual(detector.forecast(), x)
