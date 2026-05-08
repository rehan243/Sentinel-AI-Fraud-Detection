create or replace view fraud_analysis as
select 
    t.transaction_id,
    t.user_id,
    t.amount,
    t.timestamp,
    t.status,
    u.account_age,
    u.average_transaction_value,
    case 
        when t.amount > u.average_transaction_value * 2 then 'high_risk'
        when t.amount between u.average_transaction_value and u.average_transaction_value * 2 then 'medium_risk'
        else 'low_risk'
    end as risk_level,
    case 
        when t.status = 'failed' then 1
        when t.status = 'successful' then 0
        else null
    end as failed_transaction
from transactions t
join users u on t.user_id = u.user_id
where t.timestamp >= current_date - interval '30 days'
order by t.timestamp desc;

-- TODO: might want to add more filters for specific transaction types later
-- consider indexing transaction_id for performance if this gets large