# Engineering Log

Running notes on design decisions and lessons learned.


### 2026-07-10

Noticed that feature distributions for transaction amount and frequency drift significantly over time, causing model performance dips. Implemented periodic recalibration of feature thresholds, but found that overly frequent updates (weekly vs. monthly) led to increased false positives due to noise sensitivity. Balancing drift detection sensitivity with stability remains key.

### 2026-07-15

I've added a new script for automated feature engineering using LightAutoML, which has significantly sped up the initial model training process. However, I've noticed that the auto-generated features can sometimes introduce drift more rapidly than hand-crafted ones, so I've implemented a monitoring pipeline using Evidently AI to keep an eye on this. I've found that setting a threshold of 0.05 for the Population Stability Index is a good starting point for detecting drift in our fraud models.

### 2026-07-16

Added drift monitoring on top 10 features using population stability index (PSI) with a 0.1 threshold to flag shifts. Noticed PSI is sensitive to binning strategy, using quantile bins stabilized alerts better than equal-width bins, reducing false positives during normal variance. Need to balance alert sensitivity against operational noise.

### 2026-07-18

Implemented new feature engineering techniques that leverage transaction velocity and user behavior patterns for fraud detection models. Noticed that while adding derived features improved model accuracy, it also increased the risk of overfitting, especially with smaller datasets. I had to balance complexity and interpretability, deciding to limit the number of features to maintain a stable performance on unseen data.

### 2026-07-19

**Observation:** After implementing drift monitoring for our fraud models, I noticed that the false positive rate (FPR) increased by 10% during the initial monitoring period. This was due to the model's sensitivity to small changes in the data distribution, highlighting the importance of regular retraining and careful feature selection to maintain model performance.

### 2026-07-24

Added rolling window feature calculations to capture temporal spending patterns, but noticed increasing feature staleness beyond a 14-day window led to degraded model performance. Drift monitoring with population stability index (PSI) highlighted that features aggregated over longer periods mask sudden shifts in fraud behavior, so I settled on a 7-day window for a better balance between stability and responsiveness.
