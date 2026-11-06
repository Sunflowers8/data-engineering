# SQL Cheatsheet for Data Engineering

Examples use DuckDB-compatible SQL.

## 1. Basic Query

```sql
SELECT order_id, customer_id, total_amount
FROM orders
WHERE status = 'completed'
ORDER BY total_amount DESC;
```

## 2. Aggregation

```sql
SELECT
    customer_id,
    COUNT(*) AS order_count,
    SUM(total_amount) AS total_sales
FROM orders
WHERE status = 'completed'
GROUP BY customer_id;
```

## 3. Joins

```sql
SELECT
    o.order_id,
    c.full_name
FROM orders o
LEFT JOIN customers c
    ON o.customer_id = c.customer_id;
```

`INNER JOIN` returns matching rows.
`LEFT JOIN` retains every left-side row.
Check join cardinality to avoid multiplying facts.

## 4. CTEs

```sql
WITH completed_orders AS (
    SELECT *
    FROM orders
    WHERE status = 'completed'
)
SELECT COUNT(*)
FROM completed_orders;
```

## 5. Latest Record per Key

```sql
WITH ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY updated_at DESC, source_seq DESC
        ) AS rn
    FROM orders
    WHERE NULLIF(TRIM(order_id), '') IS NOT NULL
)
SELECT *
FROM ranked
WHERE rn = 1;
```

This selects one current version for each order.

## 6. Customer Ranking

```sql
WITH sales AS (
    SELECT
        customer_id,
        SUM(total_amount) AS total_sales
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
)
SELECT
    customer_id,
    total_sales,
    RANK() OVER (
        ORDER BY total_sales DESC
    ) AS sales_rank
FROM sales;
```

## 7. Running Total

```sql
SELECT
    order_ts,
    total_amount,
    SUM(total_amount) OVER (
        ORDER BY order_ts, order_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM orders;
```

## 8. LAG and LEAD

```sql
SELECT
    customer_id,
    order_ts,
    LAG(order_ts) OVER (
        PARTITION BY customer_id
        ORDER BY order_ts
    ) AS previous_order_ts
FROM orders;
```

Useful for comparing consecutive events.

## 9. Conditional Aggregation

```sql
SELECT
    COUNT(*) FILTER (
        WHERE status = 'completed'
    ) AS completed_orders,
    SUM(
        CASE
            WHEN status = 'completed'
            THEN total_amount
            ELSE 0
        END
    ) AS completed_sales
FROM orders;
```

## 10. Upsert with a Primary Key

```sql
CREATE TABLE IF NOT EXISTS customer_summary (
    customer_id VARCHAR PRIMARY KEY,
    total_sales DECIMAL(18, 2)
);

INSERT INTO customer_summary
VALUES ('C001', 500.00)
ON CONFLICT (customer_id)
DO UPDATE SET
    total_sales = excluded.total_sales;
```

## 11. Validate Uniqueness

```sql
SELECT
    order_id,
    COUNT(*) AS occurrences
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;
```

## 12. Validate Relationships

```sql
SELECT o.order_id
FROM orders o
LEFT JOIN customers c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
```

## 13. Query Performance

```sql
EXPLAIN
SELECT *
FROM orders
WHERE order_ts >= '2026-10-01'
  AND order_ts < '2026-10-03';
```

Useful optimization principles:

- Filter early when possible.
- Scan only necessary columns.
- Use date partition pruning when supported.
- Investigate expensive joins.
- Avoid unnecessary transformations.
- Use `EXPLAIN` to inspect query plans.

## 14. Interview Reminders

- Define table grain before writing joins.
- Deduplicate before calculating business metrics.
- Apply business status rules consistently.
- Handle ties deterministically.
- Separate completed sales from captured payments.
- Verify counts and totals after transformations.
