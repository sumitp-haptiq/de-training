select
sum(debit) as total_debit,
sum(credit) as total_credit
from {{ ref('staging_trial_balances') }}
having sum(debit) <> sum(credit)