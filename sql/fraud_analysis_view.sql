create or replace view fraud_analysis as 
select 
    transaction_id,
    user_id,
    transaction_date,
    amount,
    case 
        when amount > 1000 then 'high_value'
        when amount between 500 and 1000 then 'medium_value'
        else 'low_value'
    end as value_category,
    case 
        when user_id in (select user_id from flagged_users) then 'flagged'
        else 'normal'
    end as user_status,
    count(*) over (partition by user_id order by transaction_date) as transaction_count,
    avg(amount) over (partition by user_id order by transaction_date rows between unbounded preceding and current row) as avg_transaction_amount
from 
    transactions
where 
    transaction_date >= current_date - interval '1 year'
order by 
    transaction_date desc;

-- TODO: check if we need indexes on user_id or transaction_date for performance
-- that should help speed things up when querying this view