
{{ config(materialized='table') }}

SELECT
    pickup_date,
    COUNT(*) AS total_trips,
    {{ total_revenue('total_amount') }} AS total_revenue,
    ROUND(AVG(total_amount), 2) AS average_trip_revenue

FROM {{ ref('stg_taxi_trips') }}

GROUP BY pickup_date
ORDER BY pickup_date
