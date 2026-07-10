# Engineering Log

Running notes on design decisions and lessons learned.


### 2026-07-10

Noticed that feature distributions for transaction amount and frequency drift significantly over time, causing model performance dips. Implemented periodic recalibration of feature thresholds, but found that overly frequent updates (weekly vs. monthly) led to increased false positives due to noise sensitivity. Balancing drift detection sensitivity with stability remains key.
