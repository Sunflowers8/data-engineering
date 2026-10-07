# Week 4 — Data Modeling Exercises

## Exercise 1 — Define the Grain

### Question
What is the grain of `fact_taxi_trip`?

### Answer
One row represents one NYC taxi trip.

---

## Exercise 2 — E-Commerce Grain

### Question
What is the grain of `fact_order_items`?

### Answer
One row represents one product line item within one order.

---

## Exercise 3 — Fact or Dimension?

Classify the following:

| Field | Classification |
|---|---|
| trip_distance | Fact measure |
| vendor_name | Dimension attribute |
| borough | Dimension attribute |
| total_amount | Fact measure |
| payment_type_name | Dimension attribute |

---

## Exercise 4 — Measures vs Identifiers

Given:

```text
order_id
customer_id
quantity
unit_price
revenue
```

### Measures

```text
quantity
unit_price
revenue
```

### Identifiers

```text
order_id
customer_id
```

IDs identify entities or transactions. They are not automatically measures.

---

## Exercise 5 — Additive vs Semi-Additive

Daily account balances:

```text
Oct 1 = 10,000
Oct 2 = 12,000
Oct 3 = 11,000
```

Should they be summed to calculate the current balance?

### Answer
No.

Account balance is semi-additive because it can be aggregated across some dimensions but should not normally be summed across time.

---

## Exercise 6 — 1NF

Bad structure:

```text
customer_id | phone_numbers
101         | 9800000000,9811111111
```

### Question
Why does this violate 1NF?

### Answer
The field contains multiple values in one cell.

Memory:

```text
1NF = one atomic value per field
```

---

## Exercise 7 — 2NF

Composite key:

```text
(order_id, product_id)
```

Suppose:

```text
product_name
```

depends only on `product_id`.

### Question
Why is this a 2NF problem?

### Answer
`product_name` depends on only part of the composite key rather than the whole key.

This is a partial dependency.

Memory:

```text
2NF = depend on the whole key
```

---

## Exercise 8 — 3NF

Given:

```text
employee_id → department_id
department_id → department_name
```

### Question
Why can this violate 3NF?

### Answer
`department_name` depends on another non-key attribute rather than directly on the primary key.

This is a transitive dependency.

Memory:

```text
3NF = depend on nothing but the key
```

---

## Exercise 9 — Star vs Snowflake

### Scenario
The analytics team wants simple dashboard queries with fewer joins.

Which schema is generally preferable?

### Answer
Star schema.

---

## Exercise 10 — Business Key vs Surrogate Key

Given:

```text
customer_id
customer_key
```

### Answer

```text
customer_id  = Business/source key
customer_key = Warehouse surrogate key
```

The surrogate key is generated and controlled by the warehouse.

---

## Exercise 11 — Primary and Foreign Keys

Given:

```text
dim_customer.customer_key
fact_orders.customer_key
```

### Answer

```text
dim_customer.customer_key = Primary Key
fact_orders.customer_key  = Foreign Key
```

---

## Exercise 12 — Conformed Dimension

Suppose:

```text
fact_orders
fact_returns
fact_payments
```

all use the same:

```text
dim_customer
```

What kind of dimension is it?

### Answer
A conformed dimension.

---

## Exercise 13 — Bus Matrix

Given:

```text
fact_orders   → customer, product, date
fact_returns  → customer, product, date
fact_payments → customer, date
```

Which dimensions are shared by all three processes?

### Answer

```text
customer
date
```

---

## Exercise 14 — Event Modeling

Which represents an event?

```text
A. Customer name is Simran
B. Product category is Electronics
C. Order 1001 was shipped at 2:30 PM
```

### Answer

```text
C
```

An event represents something that happened at a particular time.

---

## Exercise 15 — SCD Type 1

Customer city changes:

```text
Kathmandu → Pokhara
```

If the old value is overwritten and history is not required, which SCD type is appropriate?

### Answer

```text
SCD Type 1
```

Memory:

```text
SCD1 = overwrite
```

---

## Exercise 16 — SCD Type 2

Customer city changes:

```text
Kathmandu → Pokhara
```

Historical orders must continue showing Kathmandu.

Which SCD type should be used?

### Answer

```text
SCD Type 2
```

Memory:

```text
SCD2 = preserve history
```

---

## Exercise 17 — SCD2 Records

Example:

```text
customer_key | customer_id | city      | effective_from | effective_to | is_current
7            | 205         | Kathmandu | 2026-01-01     | 2026-08-14   | false
8            | 205         | Pokhara   | 2026-08-15     | NULL         | true
```

### Question
Why are there two different `customer_key` values?

### Answer
Each historical version receives its own warehouse surrogate key.

The business key remains:

```text
customer_id = 205
```

---

## Exercise 18 — Historical Fact Lookup

Customer 101 has:

```text
customer_key 1 → Kathmandu → valid before 2026-10-01
customer_key 2 → Pokhara   → valid from 2026-10-01
```

An order was placed:

```text
2026-09-15
```

Which customer key should the fact table use?

### Answer

```text
customer_key = 1
```

The fact must reference the customer version that was valid when the event occurred.

---

## Exercise 19 — SCD2 Date Lookup

Example:

```sql
JOIN dim_customer dc
    ON o.customer_id = dc.customer_id
   AND o.order_date >= dc.effective_from
   AND (
       dc.effective_to IS NULL
       OR o.order_date <= dc.effective_to
   )
```

### Question
What does this join accomplish?

### Answer
It finds the historical customer dimension version that was valid on the order date.

---

## Exercise 20 — Date Dimension

For:

```text
2026-10-06
```

what is the `YYYYMMDD` date key?

### Answer

```text
20261006
```

---

## Exercise 21 — Dimension Lookup

Complete the vendor lookup:

```sql
JOIN dim_vendor v
    ON t.vendor_id = v.vendor_id
```

The source contains:

```text
vendor_id
```

The fact table stores:

```text
vendor_key
```

Rule:

```text
Join using business key → retrieve surrogate key
```

---

## Exercise 22 — Role-Playing Dimension

NYC Taxi has:

```text
pu_location_id
do_location_id
```

Both describe locations.

### Answer

```sql
JOIN dim_location pickup
    ON t.pu_location_id = pickup.location_id

JOIN dim_location dropoff
    ON t.do_location_id = dropoff.location_id
```

The same dimension performs two roles:

```text
Pickup location
Dropoff location
```

---

## Exercise 23 — Missing Dimension Record

The source contains:

```text
payment_type = 0
```

but the dimension contains only IDs 1–6.

### Question
What happens if an INNER JOIN is used?

### Answer
Records with `payment_type = 0` will not match and will be removed from the result.

During the NYC Taxi project, payment type 0 was added as:

```text
Flex Fare
```

---

## Exercise 24 — Data Quality Investigation

Initial date matching:

```text
total source rows = 500000
matched dates     = 499994
unmatched dates   = 6
```

Investigation found:

```text
2025-12-31 = 6 trips
```

### Solution
Add the valid missing date to `dim_date`.

Final result:

```text
unmatched_dates = 0
```

---

## Exercise 25 — E-Commerce Fact Table

Example:

```sql
CREATE TABLE fact_orders (
    order_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id INTEGER,
    customer_key INTEGER REFERENCES dim_customer(customer_key),
    date_key INTEGER REFERENCES dim_date(date_key),
    total_amount NUMERIC(12,2)
);
```

Classify:

```text
order_key    → Surrogate primary key
order_id     → Business identifier
customer_key → Foreign key
date_key     → Foreign key
total_amount → Measure
```

---

## Exercise 26 — Idempotent Load

Why can repeatedly running a plain INSERT be dangerous?

### Answer
It can create duplicate fact records.

Example protection:

```sql
WHERE NOT EXISTS (
    SELECT 1
    FROM fact_orders f
    WHERE f.order_id = o.order_id
)
```

Other options include:

```text
UNIQUE constraint
UPSERT
MERGE
```

---

# Exam-Style Practice

## Scenario

An e-commerce system contains:

```text
customers
products
orders
order_items
```

Customer city can change, and historical reporting must preserve the old city.

### Q1
What is the grain of `fact_order_items`?

**Answer:** One row per product line item within an order.

### Q2
Name three dimensions.

**Answer:**

```text
dim_customer
dim_product
dim_date
```

### Q3
Name three measures.

**Answer:**

```text
quantity
unit_price
revenue
```

### Q4
Which SCD type should be used for customer city?

**Answer:** SCD Type 2.

### Q5
Should the fact reference `customer_id` or `customer_key`?

**Answer:** `customer_key`, because each historical SCD2 version has its own surrogate key.

---

# Week 4 Exercise Checklist

- [x] Grain
- [x] Facts and dimensions
- [x] Measures
- [x] Additive/semi-additive measures
- [x] Business keys
- [x] Surrogate keys
- [x] Primary/foreign keys
- [x] 1NF
- [x] 2NF
- [x] 3NF
- [x] Star schema
- [x] Snowflake schema
- [x] Conformed dimensions
- [x] Bus matrix
- [x] Event modeling
- [x] SCD Type 1
- [x] SCD Type 2
- [x] Historical dimension lookup
- [x] Date dimension
- [x] Role-playing dimensions
- [x] Dimension lookup
- [x] Data-quality checks
- [x] Idempotency
