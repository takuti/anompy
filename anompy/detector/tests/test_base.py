from unittest import TestCase

from anompy.detector.base import BaseDetector


class BaseDetectorTestCase(TestCase):

    def test(self):
        detector = BaseDetector()

        for x in range(1, 11):
            detector.update(x)
            self.assertEqual(detector.predict(), x)
            self.assertEqual(detector.detect(threshold=(x / 2.)), True)
