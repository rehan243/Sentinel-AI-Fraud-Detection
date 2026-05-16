create or replace view fraud_analysis_view as
select 
    f.transaction_id,
    f.user_id,
    f.transaction_amount,
    f.transaction_date,
    case 
        when f.transaction_amount > 1000 then 'high_value'
        when f.transaction_amount between 500 and 1000 then 'medium_value'
        else 'low_value'
    end as value_category,
    r.risk_score,
    r.alert_status
from 
    transactions f
left join 
    risk_scores r on f.transaction_id = r.transaction_id
where 
    f.transaction_date >= current_date - interval '30 days' -- look at last 30 days
    and r.alert_status = 'active' -- only consider active alerts
order by 
    f.transaction_date desc; -- sort by date, latest first

-- TODO: add more filters if needed based on user feedback
-- maybe consider adding a group by for aggregation later on