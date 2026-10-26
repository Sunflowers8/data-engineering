
{{
    config(
        materialized='incremental',
        unique_key='pickup_date',
        incremental_strategy='merge'
    )
}}

WITH trips AS (

    SELECT
        pickup_date,
        total_amount
    FROM {{ ref('stg_taxi_trips') }}

    {% if is_incremental() %}
        WHERE pickup_date >= (
            SELECT MAX(pickup_date) - INTERVAL 1 DAY
            FROM {{ this }}
        )
    {% endif %}

)

SELECT
    pickup_date,
    COUNT(*) AS total_trips,
    ROUND(SUM(total_amount), 2) AS total_revenue
FROM trips
GROUP BY pickup_date
