
-- Standardize customer records
SELECT
    customer_id,
    full_name,
    email,
    NULLIF(TRIM(city), '') AS city,
    updated_at,
    source_seq
FROM {{ source('shopflow_raw', 'customers') }}
