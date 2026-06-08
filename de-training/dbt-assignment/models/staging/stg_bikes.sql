select
    bike_id,
    model_type as bike_model,
    rental_price,
    status
from {{ source('greenwheel', 'raw_bikes') }}
