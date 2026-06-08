
with tb as (
    select * from {{ ref('staging_trial_balances') }}
),

report as (
    select
        year,
        month,
        sum(
            case
                when category = 'Revenue'
                then period_amount
                else 0
            end
        ) as revenue,
        sum(
            case
                when category = 'Expense'
                then period_amount
                else 0
            end
        ) as expense,
        sum(
            case
                when category = 'Asset'
                then period_amount
                else 0
            end
        ) as asset
    from tb
    group by year, month
    order by year, month
)

select * from report