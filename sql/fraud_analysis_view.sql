-- this view aggregates fraud detection results by day
-- helps in analyzing trends over time

create or replace view daily_fraud_analysis as
select
    date(fraud_timestamp) as fraud_date,
    count(*) as total_frauds,
    sum(case when fraud_score > 0.5 then 1 else 0 end) as high_risk_frauds,
    sum(case when fraud_score <= 0.5 then 1 else 0 end) as low_risk_frauds,
    avg(fraud_score) as average_fraud_score
from
    fraud_records
where
    fraud_timestamp >= now() - interval '30 days' -- last 30 days
group by
    fraud_date
order by
    fraud_date desc;

-- TODO: consider adding more fields like user demographics or transaction types