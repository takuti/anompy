class BaseDetector(object):

    def __init__(self, threshold=0.):
        self.threshold = threshold
        self.x_last = 0.

    def forecast(self):
        """Forecast expected `x`.
        """
        return self.x_last

    def observe(self, x):
        """Update forecasting/detection model for observed `x`,
        and return if expected `x` could be anomaly based on the threshold.
        """
        self.x_last = x
        return self.forecast() > self.threshold
