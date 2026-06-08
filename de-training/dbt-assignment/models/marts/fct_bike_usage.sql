select
    b.bike_id,
    b.bike_model,
    sum(t.trip_cost) as total_cost,
    sum(t.trip_duration_seconds) / 60.0 as total_minutes
from {{ ref('stg_bikes') }} as b
inner join {{ source('greenwheel', 'raw_trips') }} as t
    on b.bike_id = t.bike_id
group by b.bike_id, b.bike_model
