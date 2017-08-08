from unittest import TestCase

from anompy.detector.simple_average import SimpleAverage


class SimpleAverageTestCase(TestCase):

    def test(self):
        detector = SimpleAverage()
        s = 0.

        for x in range(1, 11):
            detector.observe(x)
            s += x
            self.assertAlmostEqual(detector.forecast(), s / x, delta=1e-6)
            self.assertEqual(detector.is_anomaly(threshold=x), False)
