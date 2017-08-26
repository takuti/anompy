from collections import deque

from anompy.detector.base import BaseDetector


class AverageDetector(BaseDetector):

    def __init__(self, observed_0, window_size=None, weights=None, threshold=0.):
        self.moving_average = window_size is not None
        self.weighted = weights is not None

        if self.moving_average:
            self.window = deque([observed_0], maxlen=window_size)

            if self.weighted:
                assert window_size == len(weights)
            self.weights = weights
        else:
            self.num_observed = 1

        self.threshold = threshold
        self.average = observed_0

    def detect(self, observed_series):
        forecasted_series = []

        for observed in observed_series:
            forecasted_series.append((self.average, self.average > self.threshold))

            if self.moving_average:  # moving average
                self.window.appendleft(observed)
                if self.weighted:
                    self.average = sum([vi * wi for vi, wi in zip(self.window, self.weights)])
                else:
                    self.average = sum(self.window) / len(self.window)
            else:  # simple average
                # m_{n} = ((n - 1) m_{n-1} + x_n) / n
                # `(n - 1) m_{n-1}` returns sum of x_1, x_2, ..., x_{n-1}
                self.num_observed += 1
                self.average = self.average + (observed - self.average) / self.num_observed

        return forecasted_series
