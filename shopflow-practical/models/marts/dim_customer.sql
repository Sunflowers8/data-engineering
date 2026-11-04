
-- Customer dimension: one row per current customer

SELECT
    md5(customer_id) AS customer_key,
    customer_id,
    full_name,
    email,
    city,
    updated_at
FROM {{ ref('stg_customers') }}
