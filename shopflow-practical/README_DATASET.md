# ShopFlow Data Engineering Practical Dataset

This dataset supports the 4-hour ShopFlow Data Engineering practical examination.

## Files to use

For incremental/Python ingestion work, process the daily raw folders in this order:

1. `raw/2026-10-01/`
2. `raw/2026-10-02/`
3. Re-run `raw/2026-10-02/` to demonstrate idempotency.

Each raw folder contains:
- `customers.csv`
- `orders.csv`
- `payments.json`

`combined_for_sql/` contains both daily batches combined for convenient SQL loading and ad-hoc analysis. Use the dated raw folders for the incremental-loading/idempotency part of the exam.

## Source fields

### customers
- `source_seq`: monotonically increasing source-arrival sequence; may be used as the deterministic tie-breaker when `updated_at` ties.
- `customer_id`: business key; required.
- `full_name`
- `email`
- `city`: optional and may be blank.
- `updated_at`: source change timestamp in UTC.

### orders
- `source_seq`: deterministic source-arrival sequence.
- `order_id`: business key; required.
- `customer_id`: required for a valid business order.
- `order_ts`: business/event timestamp in UTC.
- `status`: `pending`, `completed`, or `cancelled`.
- `total_amount`: order-level sales amount.
- `updated_at`: source change/watermark timestamp in UTC.

### payments
- `source_seq`: deterministic source-arrival sequence.
- `payment_id`: payment business key; required.
- `order_id`: related order business key; required.
- `payment_ts`
- `amount`
- `method`: `card`, `wallet`, or `bank`.
- `status`: `initiated`, `failed`, `captured`, or `refunded`.
- `updated_at`: source change timestamp in UTC.

## Intentional characteristics

The files are intentionally not perfectly clean. They contain:
- repeated `customer_id`, `order_id`, and `payment_id` records with later updates;
- some records whose `updated_at` timestamps tie, requiring a deterministic tie-breaker;
- a small number of rows with missing required business keys that should be rejected/quarantined;
- late-arriving order data in the second batch whose `order_ts` belongs to the previous day;
- updates that change an earlier order/payment status;
- multiple payment attempts for some orders;
- more than one captured payment attempt for a small number of orders, so an order-level fact table must not multiply revenue;
- optional blank customer attributes.

## Business rules for the exam

- Use `updated_at` as the main incremental/watermark field unless you justify another design.
- For equal `updated_at`, `source_seq` is the supplied deterministic tie-breaker: larger `source_seq` is later.
- A current order with status `completed` contributes to completed-order sales. `cancelled` and `pending` orders do not.
- Payments should not multiply order revenue. The order remains the business grain of `fct_orders`.
- Treat rows missing required business keys as bad rows rather than valid business records.
- The same batch must be safe to run more than once without creating duplicate business records.

All timestamps use ISO-8601 UTC (`Z`) format.
