create or replace view fraud_analysis as
select 
    t.user_id,
    t.transaction_id,
    t.transaction_amount,
    t.transaction_date,
    t.fraud_score,
    case 
        when t.fraud_score > 0.8 then 'high risk'
        when t.fraud_score between 0.5 and 0.8 then 'medium risk'
        else 'low risk'
    end as risk_category,
    count(f.id) as fraud_report_count
from 
    transactions t
left join 
    fraud_reports f on t.transaction_id = f.transaction_id
group by 
    t.user_id, 
    t.transaction_id, 
    t.transaction_amount, 
    t.transaction_date, 
    t.fraud_score
order by 
    t.transaction_date desc;

-- TODO: add indexes to improve performance on large datasets