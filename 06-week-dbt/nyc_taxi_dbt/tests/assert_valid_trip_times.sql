-- Return trips that violate our business rule.
-- A dbt singular test passes when this query returns zero rows.

SELECT
    pickup_datetime,
    dropoff_datetime
FROM {{ ref('stg_taxi_trips') }}
WHERE dropoff_datetime < pickup_datetime