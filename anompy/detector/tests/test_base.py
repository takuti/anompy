from unittest import TestCase

from anompy.detector.base import BaseDetector


class BaseDetectorTestCase(TestCase):

    def test(self):
        detector = BaseDetector()

        for x in range(1, 11):
            detector.observe(x)
            self.assertEqual(detector.forecast(), x)
            self.assertEqual(detector.is_anomaly(threshold=(x / 2.)), True)
