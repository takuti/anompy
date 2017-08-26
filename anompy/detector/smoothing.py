from anompy.detector.base import BaseDetector


class ExponentialSmoothing(BaseDetector):

    def __init__(self, observed_0, alpha=0.5, threshold=0.):
        self.alpha = alpha
        self.threshold = threshold
        self.forecasted = observed_0

    def detect(self, observed_series):
        forecasted_series = []

        for observed in observed_series:
            forecasted_series.append((self.forecasted, self.forecasted > self.threshold))
            self.forecasted = self.alpha * observed + (1. - self.alpha) * self.forecasted

        return forecasted_series


class DoubleExponentialSmoothing(BaseDetector):

    def __init__(self, observed_0, alpha=0.5, beta=0.5, threshold=0.):
        self.alpha = alpha
        self.beta = beta
        self.threshold = threshold
        self.forecasted = observed_0

    def detect(self, observed_series):
        forecasted_series = []

        for observed in observed_series:
            forecasted_series.append((self.forecasted, self.forecasted > self.threshold))

            if not hasattr(self, 'level'):
                # level, trend = 1st point, 2nd point - 1st point
                self.level, self.trend = self.forecasted, observed - self.forecasted

            # update level
            self.level_last = self.level
            self.level = self.alpha * observed + (1. - self.alpha) * (self.level + self.trend)

            # update trend
            self.trend = self.beta * (self.level - self.level_last) + (1. - self.beta) * self.trend

            # combine level + trend as a forecasted value
            self.forecasted = self.level + self.trend

        return forecasted_series


class TripleExponentialSmoothing(BaseDetector):

    def __init__(self, initial_series, season_length=10, alpha=0.5, beta=0.5, gamma=0.5, threshold=0.):
        self.season_length = season_length
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.threshold = threshold

        # start creating forecast model
        self.seasonals = self.initial_seasonal_components(initial_series, season_length)
        self.level = initial_series[0]
        self.trend = self.initial_trend(initial_series, season_length)

        for i, observed in enumerate(initial_series[1:]):
            seasonal_index = (i + 1) % season_length

            # update level
            level_last = self.level
            self.level = self.alpha * (observed - self.seasonals[seasonal_index]) + (1. - self.alpha) * (self.level + self.trend)

            # update trend
            self.trend = self.beta * (self.level - level_last) + (1. - self.beta) * self.trend

            # update seasonal component
            self.seasonals[seasonal_index] = self.gamma * (observed - self.level) + (1. - self.gamma) * self.seasonals[seasonal_index]

        self.num_forecasted = 1
        self.forecasted = self.level + self.trend + self.seasonals[0]

    def detect(self, observed_series):
        forecasted_series = []

        for observed in observed_series:
            forecasted_series.append((self.forecasted, self.forecasted > self.threshold))

            self.num_forecasted += 1

            seasonal_index = (self.num_forecasted - 1) % self.season_length
            self.forecasted = self.level + self.num_forecasted * self.trend + self.seasonals[seasonal_index]

        return forecasted_series

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
