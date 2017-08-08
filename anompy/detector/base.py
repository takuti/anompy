class BaseDetector(object):

    def __init__(self):
        self.x_last = 0.

    def forecast(self):
        """Forecast expected `x`.
        """
        return self.x_last

    def observe(self, x):
        """Update forecasting/detection model for observed `x`.
        """
        self.x_last = x

    def is_anomaly(self, threshold=0.):
        """Forecast expected `x` and detect if it could be anomaly based on the threshold.
        """
        return self.forecast() > threshold
