
{{
    config(
        materialized='incremental',
        unique_key='order_id',
        incremental_strategy='delete+insert'
    )
}}

-- One fact row per business order.
-- Changes to orders OR payments must refresh the order.

WITH payment_summary AS (
    SELECT
        order_id,
        SUM(
            CASE
                WHEN status = 'captured' THEN amount
                ELSE 0
            END
        ) AS captured_payment_amount,
        MAX(updated_at) AS payment_updated_at
    FROM {{ ref('stg_payments') }}
    GROUP BY order_id
),

order_facts AS (
    SELECT
        o.order_id,
        c.customer_key,
        o.customer_id,
        o.order_date,
        o.status,
        o.total_amount,

        CASE
            WHEN o.status = 'completed' THEN o.total_amount
            ELSE 0
        END AS completed_sales_amount,

        COALESCE(p.captured_payment_amount, 0)
            AS captured_payment_amount,

        o.updated_at,

        GREATEST(
            o.updated_at,
            COALESCE(p.payment_updated_at, o.updated_at)
        ) AS last_changed_at

    FROM {{ ref('stg_orders') }} o

    LEFT JOIN {{ ref('dim_customer') }} c
        ON o.customer_id = c.customer_id

    LEFT JOIN payment_summary p
        ON o.order_id = p.order_id
)

SELECT *
FROM order_facts

{% if is_incremental() %}
WHERE last_changed_at >= (
    SELECT COALESCE(
        MAX(last_changed_at),
        TIMESTAMPTZ '1900-01-01 00:00:00+00'
    )
    FROM {{ this }}
)
{% endif %}
