from anompy.detector.base import BaseDetector


class SimpleAverage(BaseDetector):

    def __init__(self):
        self.avg = 0.
        self.cnt = 0.

    def forecast(self):
        return self.avg

    def observe(self, x):
        """m_{n} = ((n - 1) m_{n-1} + x_n) / n

        `(n - 1) m_{n-1}` returns sum of x_1, x_2, ..., x_{n-1}

        """
        self.cnt += 1
        self.avg = self.avg + (x - self.avg) / self.cnt
