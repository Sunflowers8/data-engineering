
-- Standardize payment records
SELECT
    payment_id,
    order_id,
    payment_ts,
    CAST(amount AS DECIMAL(18, 2)) AS amount,
    method,
    LOWER(TRIM(status)) AS status,
    updated_at,
    source_seq
FROM {{ source('shopflow_raw', 'payments') }}
