from collections import deque

from anompy.detector.base import BaseDetector


class AverageDetector(BaseDetector):

    def __init__(self, window_size=None, weights=None):
        self.moving_average = window_size is not None
        if self.moving_average:
            self.window = deque(maxlen=window_size)
            self.weights = weights
        else:
            self.cnt = 0.
        self.avg = 0.

    def forecast(self):
        return self.avg

    def observe(self, x):
        if self.moving_average:  # moving average
            self.window.append(x)
            if self.weights is not None:
                self.avg = sum([xi * wi for xi, wi in zip(self.window, self.weights)])
            else:
                self.avg = sum(self.window) / len(self.window)
        else:  # simple average
            # m_{n} = ((n - 1) m_{n-1} + x_n) / n
            # `(n - 1) m_{n-1}` returns sum of x_1, x_2, ..., x_{n-1}
            self.cnt += 1
            self.avg = self.avg + (x - self.avg) / self.cnt
