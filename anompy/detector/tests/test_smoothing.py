from unittest import TestCase

from anompy.detector.smoothing import ExponentialSmoothing, DoubleExponentialSmoothing, TripleExponentialSmoothing


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


class DoubleExponentialSmoothingTestCase(TestCase):

    def test(self):
        detector = DoubleExponentialSmoothing(alpha=.9, beta=.9)

        series = [3, 10, 12, 13, 12, 10, 12]
        expected = [3, 17.0, 15.45, 14.210500000000001, 11.396044999999999, 8.183803049999998, 12.753698384500002, 13.889016464000003]
        eps = 1e-6

        for i in range(len(series)):
            anomaly = detector.observe(series[i])
            self.assertTrue(anomaly)
            self.assertAlmostEqual(detector.forecast(), expected[i], delta=eps)


class TripleExponentialSmoothingTestCase(TestCase):

    def setUp(self):
        self.series = [30, 21, 29, 31, 40, 48, 53, 47, 37, 39, 31, 29, 17, 9, 20, 24, 27, 35, 41, 38,
                       27, 31, 27, 26, 21, 13, 21, 18, 33, 35, 40, 36, 22, 24, 21, 20, 17, 14, 17, 19,
                       26, 29, 40, 31, 20, 24, 18, 26, 17, 9, 17, 21, 28, 32, 46, 33, 23, 28, 22, 27,
                       18, 8, 17, 21, 31, 34, 44, 38, 31, 30, 26, 32]
        self.slen = 12

    def test_initial_trend(self):
        initial_trend = TripleExponentialSmoothing.initial_trend(self.series, self.slen)
        expected = -0.7847222222222222
        self.assertAlmostEqual(initial_trend, expected, delta=1e-6)

    def test_initial_seasonal_components(self):
        components = TripleExponentialSmoothing.initial_seasonal_components(self.series, self.slen)
        expected = [-7.4305555555555545, -15.097222222222221, -7.263888888888888, -5.097222222222222, 3.402777777777778, 8.069444444444445, 16.569444444444446, 9.736111111111112, -0.7638888888888887, 1.902777777777778, -3.263888888888889, -0.7638888888888887]
        eps = 1e-6

        for i in range(self.slen):
            self.assertAlmostEqual(components[i], expected[i], delta=eps)

    def test(self):
        detector = TripleExponentialSmoothing(season_length=self.slen, alpha=0.716, beta=0.029, gamma=0.993)

        for x in self.series:
            self.assertTrue(detector.observe(x))

        expected = [22.42511411230803, 15.343371755223066, 24.14282581581347, 27.02259921391996, 35.31139046245393, 38.999014669337356, 49.243283875692654, 40.84636009563803, 31.205180503707012, 32.96259980122959, 28.5164783238384, 32.30616336737171]
        eps = 1e-6

        for i in range(self.slen):
            self.assertAlmostEqual(detector.forecast(), expected[i], delta=eps)
