class BaseDetector(object):

    def __init__(self):
        self.x_last = 0.

    def predict(self):
        """Forecast expected `x`.
        """
        return self.x_last

    def detect(self, threshold=0.):
        """Forecast expected `x` and detect if it could be anomaly based on the threshold.
        """
        return self.predict() > threshold

    def update(self, x):
        """Update forecasting/detection model for observed `x`.
        """
        self.x_last = x
