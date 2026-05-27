create or replace view user_fraud_analysis as
select 
    u.user_id,
    u.email,
    u.created_at,
    count(t.transaction_id) as transaction_count,
    sum(case when t.status = 'failed' then 1 else 0 end) as failed_transactions,
    sum(case when t.status = 'successful' then t.amount else 0 end) as total_amount,
    avg(t.amount) as average_transaction_amount,
    case 
        when sum(case when t.status = 'failed' then 1 else 0 end) > 5 then 'high risk'
        when count(t.transaction_id) > 20 then 'medium risk'
        else 'low risk'
    end as risk_level
from 
    users u
left join 
    transactions t on u.user_id = t.user_id
where 
    u.created_at >= current_date - interval '1 year'
group by 
    u.user_id, u.email, u.created_at
order by 
    risk_level desc; 

-- TODO: update this view to include more user demographics if needed