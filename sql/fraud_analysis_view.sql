create or replace view fraud_analysis_view as
select 
    f.transaction_id,
    f.user_id,
    f.transaction_amount,
    f.transaction_date,
    f.risk_score,
    case 
        when f.risk_score > 80 then 'high'
        when f.risk_score between 50 and 80 then 'medium'
        else 'low'
    end as risk_category,
    u.user_name,
    u.account_status
from 
    fraud_transactions f
join 
    users u on f.user_id = u.id
where 
    f.transaction_date >= current_date - interval '30 days'
    and u.account_status = 'active'
order by 
    f.transaction_date desc;

-- TODO: maybe add more filters or group by user_id for summary stats