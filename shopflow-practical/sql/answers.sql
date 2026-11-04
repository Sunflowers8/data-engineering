-- Question 2A: Latest customer record

WITH ranked_customers AS (
    SELECT
        customer_id,
        full_name,
        email,
        city,
        updated_at,
        source_seq,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY updated_at DESC, source_seq DESC
        ) AS row_num
    FROM read_csv_auto('combined_for_sql/customers_all.csv')
    WHERE customer_id IS NOT NULL
      AND TRIM(customer_id) <> ''
)

SELECT
    customer_id,
    full_name,
    email,
    city,
    updated_at
FROM ranked_customers
WHERE row_num = 1
ORDER BY customer_id;


-- Question 2B: Latest order record

WITH ranked_orders AS (
    SELECT
        order_id,
        customer_id,
        order_ts,
        status,
        total_amount,
        updated_at,
        source_seq,
        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY updated_at DESC, source_seq DESC
        ) AS row_num
    FROM read_csv_auto('combined_for_sql/orders_all.csv')
    WHERE order_id IS NOT NULL
      AND TRIM(order_id) <> ''
      AND customer_id IS NOT NULL
      AND TRIM(customer_id) <> ''
)

SELECT
    order_id,
    customer_id,
    order_ts,
    status,
    total_amount,
    updated_at
FROM ranked_orders
WHERE row_num = 1
ORDER BY order_id;

-- Question 2C: Daily completed revenue

WITH latest_orders AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY updated_at DESC, source_seq DESC
        ) AS row_num
    FROM read_csv_auto('combined_for_sql/orders_all.csv')
    WHERE NULLIF(TRIM(order_id), '') IS NOT NULL
      AND NULLIF(TRIM(customer_id), '') IS NOT NULL
)

SELECT
    CAST(order_ts AT TIME ZONE 'UTC' AS DATE) AS order_date,
    COUNT(*) AS completed_order_count,
    ROUND(SUM(total_amount), 2) AS total_completed_sales
FROM latest_orders
WHERE row_num = 1
  AND status = 'completed'
GROUP BY order_date
ORDER BY order_date;

-- Question 2D: Top 3 customers by completed sales

WITH latest_orders AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY updated_at DESC, source_seq DESC
        ) AS row_num
    FROM read_csv_auto('combined_for_sql/orders_all.csv')
    WHERE NULLIF(TRIM(order_id), '') IS NOT NULL
      AND NULLIF(TRIM(customer_id), '') IS NOT NULL
),

customer_sales AS (
    SELECT
        customer_id,
        COUNT(*) AS completed_order_count,
        ROUND(SUM(total_amount), 2) AS total_sales
    FROM latest_orders
    WHERE row_num = 1
      AND status = 'completed'
    GROUP BY customer_id
),

ranked_customers AS (
    SELECT *,
        RANK() OVER (
            ORDER BY total_sales DESC
        ) AS sales_rank
    FROM customer_sales
)

SELECT
    customer_id,
    completed_order_count,
    total_sales,
    sales_rank
FROM ranked_customers
WHERE sales_rank <= 3
ORDER BY sales_rank, customer_id;

-- Question 2E: Performance reasoning
--
-- Partitioning the orders table by order date allows the
-- warehouse to scan only the dates required by a query.
-- This can reduce the amount of data processed and improve
-- query performance, especially for daily revenue reports.
-- Clustering by customer_id can make customer-specific
-- queries more efficient by organizing related records.
-- However, these optimizations offer limited benefits
-- for small tables or queries that scan the entire dataset.