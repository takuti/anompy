from anompy.detector.base import BaseDetector


class ExponentialSmoothing(BaseDetector):

    def __init__(self, alpha=0.5, threshold=0.):
        self.alpha = alpha
        self.threshold = threshold
        self.x_last = 0.

    def forecast(self):
        assert hasattr(self, 'forecast_cache'), 'observe at least 1 data point first'
        self.forecast_cache = self.alpha * self.x_last + (1. - self.alpha) * self.forecast_cache
        return self.forecast_cache

    def observe(self, x):
        if not hasattr(self, 'forecast_cache'):
            self.forecast_cache = x
        self.x_last = x
        return self.forecast_cache > self.threshold


class DoubleExponentialSmoothing(BaseDetector):

    def __init__(self, alpha=0.5, beta=0.5, threshold=0.):
        self.alpha = alpha
        self.beta = beta
        self.threshold = threshold
        self.x_last = 0.

    def forecast(self):
        assert hasattr(self, 'x_last'), 'observe at least 1 data point first'

        if not hasattr(self, 'trend'):  # only 1 point has been observed
            return self.x_last

        self.level_cache, self.level = self.level, self.alpha * self.x_last + (1. - self.alpha) * (self.level + self.trend)
        self.trend = self.beta * (self.level - self.level_cache) + (1. - self.beta) * self.trend

        return self.level + self.trend

    def observe(self, x):
        self.x_last = x

        if not hasattr(self, 'level'):  # 1st level = 1st point
            self.level = x
            return x > self.threshold

        if not hasattr(self, 'trend'):  # 2nd level = 1st point
            self.level, self.trend = self.level, x - self.level

        return (self.level + self.trend) > self.threshold


class TripleExponentialSmoothing(BaseDetector):

    def __init__(self, season_length=10, alpha=0.5, beta=0.5, gamma=0.5, threshold=0.):
        self.season_length = season_length
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.threshold = threshold
        self.series = []

    def forecast(self):
        assert len(self.series) >= self.season_length, 'at least one season should be observed'

        if not hasattr(self, 'seasonals'):  # start creating forecast model
            self.seasonals = self.initial_seasonal_components(self.series, self.season_length)
            self.level = self.series[0]
            self.trend = self.initial_trend(self.series, self.season_length)
            for i in range(1, len(self.series)):
                x = self.series[i]
                component_index = i % self.season_length

                last_level, self.level = self.level, self.alpha * (x - self.seasonals[component_index]) + (1. - self.alpha) * (self.level + self.trend)
                self.trend = self.beta * (self.level - last_level) + (1. - self.beta) * self.trend
                self.seasonals[component_index] = self.gamma * (x - self.level) + (1. - self.gamma) * self.seasonals[component_index]

            self.forecast_count = 0

        self.forecast_count += 1

        forecast_component_index = (self.forecast_count + len(self.series) - 1) % self.season_length
        return (self.level + self.forecast_count * self.trend) + self.seasonals[forecast_component_index]

    def observe(self, x):
        if hasattr(self, 'forecast_count'):  # already called `forecast()`, so we cannot update seasonality model
            return self.forecast() > self.threshold
        self.series.append(x)
        return x > self.threshold

    @staticmethod
    def initial_trend(series, season_length):
        accum_trend_average = 0.
        for i in range(season_length):
            # difference between neighbor seasons' i-th points (= `season_length` points from i to i+season_length)
            trend_average = float(series[i + season_length] - series[i]) / season_length
            accum_trend_average += trend_average
        return accum_trend_average / season_length

    @staticmethod
    def initial_seasonal_components(series, season_length):
        """Each seasonal point is estimated based on initial value of component.
        """
        n_seasons = int(len(series) / season_length)
        season_averages = [0.] * n_seasons
        for s in range(n_seasons):
            head = season_length * s
            tail = head + season_length
            season_averages[s] = sum(series[head:tail]) / float(season_length)

        components = [0.] * season_length
        for i in range(season_length):
            # sum of difference between each season's i-th point of series and average value of the corresponding season
            accum_deviation = 0.
            for s in range(n_seasons):
                j = s * season_length + i
                accum_deviation += (series[j] - season_averages[s])
            components[i] = accum_deviation / n_seasons

        return components
