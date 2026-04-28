-- ops queries for fraud; tuned for explainable charts not cute sql

-- false positive rate by customer segment: where manual review burns time
SELECT segment,
       sum(case when predicted_fraud and not actual_fraud then 1 else 0 end)::float
         / nullif(sum(case when predicted_fraud then 1 else 0 end), 0) AS fpr_among_flags,
       count(*) AS volume
FROM fraud_eval_snapshot
WHERE eval_date > current_date - interval '30 days'
GROUP BY segment
ORDER BY fpr_among_flags DESC NULLS LAST;

-- model drift: score distribution shift week over week
SELECT date_trunc('week', scored_at) AS week,
       avg(model_score) AS avg_score,
       stddev_pop(model_score) AS std_score
FROM fraud_scores
WHERE scored_at > now() - interval '180 days'
GROUP BY 1
ORDER BY 1;

-- alert routing stats: helps tune thresholds per channel
SELECT route_channel,
       count(*) AS alerts,
       avg(latency_to_action_sec) AS avg_latency_sec
FROM fraud_alerts
WHERE created_at > now() - interval '14 days'
GROUP BY route_channel;

-- top features pushing scores up: sanity check after retrain
SELECT feature_name,
       avg(shap_value) AS mean_shap
FROM fraud_explanations
WHERE scored_at > now() - interval '7 days'
GROUP BY feature_name
ORDER BY abs(mean_shap) DESC
LIMIT 25;

CREATE INDEX IF NOT EXISTS idx_fraud_scores_time ON fraud_scores (scored_at);
CREATE INDEX IF NOT EXISTS idx_fraud_alerts_channel ON fraud_alerts (route_channel, created_at);

-- catch rate vs precision tradeoff by score bucket; helps pick a threshold
SELECT width_bucket(model_score, 0.0, 1.0, 20) AS bucket,
       count(*) AS n,
       sum(case when actual_fraud then 1 else 0 end)::float / nullif(count(*), 0) AS recall_proxy
FROM fraud_scores fs
JOIN fraud_labels fl ON fl.entity_id = fs.entity_id
WHERE fs.scored_at > now() - interval '30 days'
GROUP BY bucket
ORDER BY bucket;

-- queue depth snapshot: spikes line up with bad deploys more often than you expect
SELECT captured_at,
       queue_depth,
       oldest_waiting_sec
FROM fraud_review_queue_snapshots
WHERE captured_at > now() - interval '7 days'
ORDER BY captured_at DESC
LIMIT 500;
