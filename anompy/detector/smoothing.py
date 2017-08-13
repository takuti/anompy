from anompy.detector.base import BaseDetector


class ExponentialSmoothing(BaseDetector):

    def __init__(self, alpha=0.5):
        self.alpha = alpha
        self.x_last = 0.

    def forecast(self):
        assert hasattr(self, 'forecast_cache'), 'observe at least 1 data point first'
        self.forecast_cache = self.alpha * self.x_last + (1. - self.alpha) * self.forecast_cache
        return self.forecast_cache

    def observe(self, x):
        if not hasattr(self, 'forecast_cache'):
            self.forecast_cache = x
        self.x_last = x

    def is_anomaly(self, threshold=0.):
        return self.forecast_cache > threshold
