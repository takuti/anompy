from collections import deque

from anompy.detector.base import BaseDetector


class AverageDetector(BaseDetector):

    def __init__(self, window_size=None):
        self.moving_average = window_size is not None
        if self.moving_average:
            self.window_size = window_size
            self.window = deque(maxlen=window_size)
        else:
            self.cnt = 0.
        self.avg = 0.

    def forecast(self):
        return self.avg

    def observe(self, x):
        if self.moving_average:  # moving average
            self.window.append(x)
            self.avg = sum(self.window) / self.window_size
        else:  # simple average
            # m_{n} = ((n - 1) m_{n-1} + x_n) / n
            # `(n - 1) m_{n-1}` returns sum of x_1, x_2, ..., x_{n-1}
            self.cnt += 1
            self.avg = self.avg + (x - self.avg) / self.cnt
