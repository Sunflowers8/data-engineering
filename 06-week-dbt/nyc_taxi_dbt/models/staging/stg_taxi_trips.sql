
{{ config(materialized='view') }}

WITH source_data AS (
    SELECT *
    FROM {{ source('nyc_taxi', 'taxi_native') }}
),

renamed AS (
    SELECT
        CAST(VendorID AS BIGINT) AS vendor_id,
        CAST(tpep_pickup_datetime AS TIMESTAMP) AS pickup_datetime,
        TRY_CAST(tpep_dropoff_datetime AS TIMESTAMP) AS dropoff_datetime,
        CAST(PULocationID AS BIGINT) AS pickup_location_id,
        CAST(DOLocationID AS BIGINT) AS dropoff_location_id,
        CAST(payment_type AS BIGINT) AS payment_type_id,
        passenger_count,
        trip_distance,
        fare_amount,
        tip_amount,
        tolls_amount,
        total_amount,
        trip_duration_minutes,
        pickup_date
    FROM source_data
)

SELECT *
FROM renamed
