create or replace view fraud_analysis_view as
select 
    f.transaction_id,
    f.amount,
    f.timestamp,
    f.user_id,
    u.account_age,
    f.location,
    case 
        when f.amount > 1000 then 'high risk'
        when f.amount between 500 and 1000 then 'medium risk'
        else 'low risk'
    end as risk_level,
    sum(case when t.transaction_type = 'refund' then 1 else 0 end) as refund_count,
    count(t.transaction_id) as total_transactions,
    count(distinct f.user_id) over (partition by f.location) as user_count_in_location
from 
    transactions f
join 
    users u on f.user_id = u.user_id
left join 
    transactions t on f.user_id = t.user_id and f.timestamp > t.timestamp
where 
    f.timestamp >= current_date - interval '30 days' 
group by 
    f.transaction_id, f.amount, f.timestamp, f.user_id, u.account_age, f.location
order by 
    f.timestamp desc
-- TODO: consider adding more filters for better granularity