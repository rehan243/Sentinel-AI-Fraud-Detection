# Engineering Log

Running notes on design decisions and lessons learned.


### 2026-07-10

Noticed that feature distributions for transaction amount and frequency drift significantly over time, causing model performance dips. Implemented periodic recalibration of feature thresholds, but found that overly frequent updates (weekly vs. monthly) led to increased false positives due to noise sensitivity. Balancing drift detection sensitivity with stability remains key.

### 2026-07-15

I've added a new script for automated feature engineering using LightAutoML, which has significantly sped up the initial model training process. However, I've noticed that the auto-generated features can sometimes introduce drift more rapidly than hand-crafted ones, so I've implemented a monitoring pipeline using Evidently AI to keep an eye on this. I've found that setting a threshold of 0.05 for the Population Stability Index is a good starting point for detecting drift in our fraud models.

### 2026-07-16

Added drift monitoring on top 10 features using population stability index (PSI) with a 0.1 threshold to flag shifts. Noticed PSI is sensitive to binning strategy, using quantile bins stabilized alerts better than equal-width bins, reducing false positives during normal variance. Need to balance alert sensitivity against operational noise.
