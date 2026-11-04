
-- Standardize order records
SELECT
    order_id,
    customer_id,
    order_ts,
    CAST(order_ts AT TIME ZONE 'UTC' AS DATE) AS order_date,
    LOWER(TRIM(status)) AS status,
    CAST(total_amount AS DECIMAL(18, 2)) AS total_amount,
    updated_at,
    source_seq
FROM {{ source('shopflow_raw', 'orders') }}
