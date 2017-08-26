class BaseDetector(object):

    def __init__(self, observed_0, threshold=0.):
        self.threshold = threshold
        self.observed_last = observed_0

    def detect(self, observed_series):
        """Launch forecasting for each observed data point based on a model.
        Return labeled forecasted series if each observed data point is anomaly or not.

        Args:
            observed_series (list of float): Observed series.

        Returns:
            list of (float, boolean): Forecasted series with anomaly label.

        """
        forecasted_series = []

        for observed in observed_series:
            forecasted_series.append((self.observed_last, self.observed_last > self.threshold))
            self.observed_last = observed

        return forecasted_series
