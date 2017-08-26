class BaseDetector(object):

    def __init__(self, observed, threshold=0.):
        self.threshold = threshold
        self.observed_last = observed

    def detect(self, observed_series):
        """Launch forecasting for each observed data point based on a model.
        Return labeled forecasted series if each observed data point is anomaly or not.

        Args:
            observed_series (list of float): Observed series.

        Returns:
            list of (float, boolean): Forecasted series with anomaly label.

        """
        expected_series = []

        for observed in observed_series:
            expected_series.append((self.observed_last, self.observed_last > self.threshold))
            self.observed_last = observed

        return expected_series
