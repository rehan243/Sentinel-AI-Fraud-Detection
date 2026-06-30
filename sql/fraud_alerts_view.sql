-- this view gives us a consolidated view of fraud alerts 
-- across different categories with a risk score

CREATE OR REPLACE VIEW fraud_alerts_view AS
SELECT 
    fa.alert_id,
    fa.user_id,
    fa.alert_type,
    fa.created_at,
    fa.risk_score,
    u.name AS user_name,
    u.email AS user_email,
    COUNT(*) OVER (PARTITION BY fa.alert_type) AS alert_count
FROM 
    fraud_alerts fa
JOIN 
    users u ON fa.user_id = u.id
WHERE 
    fa.created_at >= CURRENT_DATE - INTERVAL '30 days' 
    AND fa.risk_score > 50 -- consider only high-risk alerts
ORDER BY 
    fa.created_at DESC;

-- TODO: consider adding filters for specific alert types
-- to focus on the most critical ones for analysis