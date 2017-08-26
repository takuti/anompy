from collections import deque

from anompy.detector.base import BaseDetector


class AverageDetector(BaseDetector):

    def __init__(self, observed, window_size=None, weights=None, threshold=0.):
        self.moving_average = window_size is not None
        if self.moving_average:
            self.window = deque(maxlen=window_size)
            self.window.appendleft(observed)
            if weights is not None:
                assert window_size == len(weights)
            self.weights = weights
        else:
            self.cnt = 1
        self.threshold = threshold
        self.avg = observed

    def detect(self, observed_series):
        expected_series = []

        for observed in observed_series:
            expected_series.append((self.avg, self.avg > self.threshold))

            if self.moving_average:  # moving average
                self.window.appendleft(observed)
                if self.weights is not None:
                    self.avg = sum([xi * wi for xi, wi in zip(self.window, self.weights)])
                else:
                    self.avg = sum(self.window) / len(self.window)
            else:  # simple average
                # m_{n} = ((n - 1) m_{n-1} + x_n) / n
                # `(n - 1) m_{n-1}` returns sum of x_1, x_2, ..., x_{n-1}
                self.cnt += 1
                self.avg = self.avg + (observed - self.avg) / self.cnt

        return expected_series
