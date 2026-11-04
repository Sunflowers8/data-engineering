
-- Payment reconciliation
-- Identify orders where captured payments
-- differ from completed-order sales.

SELECT
    order_id,
    status,
    completed_sales_amount,
    captured_payment_amount,
    ROUND(
        captured_payment_amount - completed_sales_amount,
        2
    ) AS difference
FROM analytics.fct_orders
WHERE captured_payment_amount <> completed_sales_amount
ORDER BY order_id;
