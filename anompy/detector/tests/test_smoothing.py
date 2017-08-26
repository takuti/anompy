from unittest import TestCase

from anompy.detector.smoothing import ExponentialSmoothing, DoubleExponentialSmoothing, TripleExponentialSmoothing


class ExponentialSmoothingTestCase(TestCase):

    def test(self):
        detector = ExponentialSmoothing(3, alpha=.1)

        observed_series = [10, 12, 13, 12, 10, 12]

        forecasted_series = detector.detect(observed_series)
        self.assertEqual(len(observed_series), len(forecasted_series))

        truth_series = [3., 3.7, 4.53, 5.377, 6.0393, 6.43537, 6.991833]
        self.assertEqual(len(observed_series), len(truth_series) - 1)

        eps = 1e-6

        for (forecasted, anomaly), truth in zip(forecasted_series, truth_series):
            self.assertTrue(anomaly)
            self.assertAlmostEqual(forecasted, truth, delta=eps)

        self.assertAlmostEqual(detector.forecasted, truth_series[-1], delta=eps)


class DoubleExponentialSmoothingTestCase(TestCase):

    def test(self):
        detector = DoubleExponentialSmoothing(3, alpha=.9, beta=.9)

        observed_series = [10, 12, 13, 12, 10, 12]

        forecasted_series = detector.detect(observed_series)
        self.assertEqual(len(observed_series), len(forecasted_series))

        truth_series = [3, 17.0, 15.45, 14.210500000000001, 11.396044999999999, 8.183803049999998, 12.753698384500002]
        self.assertEqual(len(observed_series), len(truth_series) - 1)

        eps = 1e-6

        for (forecasted, anomaly), truth in zip(forecasted_series, truth_series):
            self.assertTrue(anomaly)
            self.assertAlmostEqual(forecasted, truth, delta=eps)

        self.assertAlmostEqual(detector.forecasted, truth_series[-1], delta=eps)


class TripleExponentialSmoothingTestCase(TestCase):

    def setUp(self):
        self.series = [30, 21, 29, 31, 40, 48, 53, 47, 37, 39, 31, 29, 17, 9, 20, 24, 27, 35, 41, 38,
                       27, 31, 27, 26, 21, 13, 21, 18, 33, 35, 40, 36, 22, 24, 21, 20, 17, 14, 17, 19,
                       26, 29, 40, 31, 20, 24, 18, 26, 17, 9, 17, 21, 28, 32, 46, 33, 23, 28, 22, 27,
                       18, 8, 17, 21, 31, 34, 44, 38, 31, 30, 26, 32]
        self.slen = 12

    def test_initial_trend(self):
        initial_trend = TripleExponentialSmoothing.initial_trend(self.series, self.slen)
        forecasted = -0.7847222222222222
        self.assertAlmostEqual(initial_trend, forecasted, delta=1e-6)

    def test_initial_seasonal_components(self):
        components = TripleExponentialSmoothing.initial_seasonal_components(self.series, self.slen)
        forecasted = [-7.4305555555555545, -15.097222222222221, -7.263888888888888, -5.097222222222222, 3.402777777777778, 8.069444444444445, 16.569444444444446, 9.736111111111112, -0.7638888888888887, 1.902777777777778, -3.263888888888889, -0.7638888888888887]
        eps = 1e-6

        for i in range(self.slen):
            self.assertAlmostEqual(components[i], forecasted[i], delta=eps)

    def test(self):
        detector = TripleExponentialSmoothing(self.series, season_length=self.slen, alpha=0.716, beta=0.029, gamma=0.993)

        forecasted_series = detector.detect([0.] * self.slen)
        self.assertEqual(len(forecasted_series), self.slen)

        truth_series = [22.42511411230803, 15.343371755223066, 24.14282581581347, 27.02259921391996, 35.31139046245393, 38.999014669337356, 49.243283875692654, 40.84636009563803, 31.205180503707012, 32.96259980122959, 28.5164783238384, 32.30616336737171]
        self.assertEqual(len(forecasted_series), len(truth_series))

        eps = 1e-6

        for (forecasted, anomaly), truth in zip(forecasted_series, truth_series):
            self.assertTrue(anomaly)
            self.assertAlmostEqual(forecasted, truth, delta=eps)
