from anompy.detector.base import BaseDetector


class ExponentialSmoothing(BaseDetector):

    def __init__(self, alpha=0.5):
        self.alpha = alpha
        self.x_last = 0.

    def forecast(self):
        assert hasattr(self, 'cache'), 'observe at least 1 data point first'
        self.cache = self.alpha * self.x_last + (1. - self.alpha) * self.cache
        return self.cache

    def observe(self, x):
        if not hasattr(self, 'cache'):
            self.cache = x
        self.x_last = x

    def is_anomaly(self, threshold=0.):
        return self.cache > threshold
