select
    user_id,
    upper(user_name) as user_name,
    lower(email) as email,
    created_at
from {{ source('greenwheel', 'raw_users') }}
