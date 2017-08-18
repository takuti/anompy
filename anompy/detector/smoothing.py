from anompy.detector.base import BaseDetector


class ExponentialSmoothing(BaseDetector):

    def __init__(self, alpha=0.5, threshold=0.):
        self.alpha = alpha
        self.threshold = threshold
        self.x_last = 0.

    def forecast(self):
        assert hasattr(self, 'forecast_cache'), 'observe at least 1 data point first'
        self.forecast_cache = self.alpha * self.x_last + (1. - self.alpha) * self.forecast_cache
        return self.forecast_cache

    def observe(self, x):
        if not hasattr(self, 'forecast_cache'):
            self.forecast_cache = x
        self.x_last = x
        return self.forecast_cache > self.threshold


class DoubleExponentialSmoothing(BaseDetector):

    def __init__(self, alpha=0.5, beta=0.5, threshold=0.):
        self.alpha = alpha
        self.beta = beta
        self.threshold = threshold
        self.x_last = 0.

    def forecast(self):
        assert hasattr(self, 'x_last'), 'observe at least 1 data point first'

        if not hasattr(self, 'trend'):  # only 1 point has been observed
            return self.x_last

        self.level_cache, self.level = self.level, self.alpha * self.x_last + (1. - self.alpha) * (self.level + self.trend)
        self.trend = self.beta * (self.level - self.level_cache) + (1. - self.beta) * self.trend

        return self.level + self.trend

    def observe(self, x):
        self.x_last = x

        if not hasattr(self, 'level'):  # 1st level = 1st point
            self.level = x
            return x > self.threshold

        if not hasattr(self, 'trend'):  # 2nd level = 1st point
            self.level, self.trend = self.level, x - self.level

        return (self.level + self.trend) > self.threshold
