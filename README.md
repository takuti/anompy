anompy
===

**anompy** is a Python package of forecasting and anomaly detection algorithms.

## Installation

```
$ pip install git+https://github.com/takuti/anompy.git
```

## Usage

Generate dummy time-series:

```py
>>> import random
>>> series = [random.random() for i in range(10)]
>>> series
[0.29749066250070444, 0.17992724665541393, 0.24201406949661697, 0.3467356134915024, 0.45318143064943217, 0.20825014566859423, 0.597497516445304, 0.5442072127508967, 0.1920841531842088, 0.2711214524302953]
```

Import `BaseDetector` which simply returns the last observed data point as a forecasted value, and create a detector with initial data point (i.e., training sample) and threshold:

```py
>>> from anompy.detector.base import BaseDetector
>>> detector = BaseDetector(series[0], threshold=0.5)
```

Get forecasted time-series and their anomaly labels by calling `detect()` method:

```py
>>> detector.detect(series[1:])
[(0.29749066250070444, False), (0.17992724665541393, False), (0.24201406949661697, False), (0.3467356134915024, False), (0.45318143064943217, False), (0.20825014566859423, False), (0.597497516445304, True), (0.5442072127508967, True), (0.1920841531842088, False)]
```

See [this notebook](https://gist.github.com/takuti/36d54e432a49424bb31d948926cd49b4) for more examples.

## Algorithm

anompy currently supports following algorithms:

- `BaseDetector`
    - Directly use the last observation as a forecasted value, and detect anomaly based on threshold.
- `AverageDetector`
    - Forecast either global average, simple moving average or weighted moving average.
- `ExponentialSmoothing`, `DoubleExponentialSmoothing`, and `TripleExponentialSmoothing`
    - See ["Exponential smoothing" on Wikipedia](https://en.wikipedia.org/wiki/Exponential_smoothing).
    - Triple exponential smoothing is also known as Holt-Winters method.
- Experimental
    - `ChangeFinder`
    - `SingularSpectrumTransform`
    - `StreamAnomalyDetector`