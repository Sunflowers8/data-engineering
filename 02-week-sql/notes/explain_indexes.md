# EXPLAIN, Query Optimization and Indexes

## Overview

Week 2 introduced query-performance analysis using a real PostgreSQL table containing **500,000 NYC Yellow Taxi trip records**.

The goal was to understand how PostgreSQL executes a query and how indexing can affect its execution strategy.

---

## EXPLAIN

`EXPLAIN` displays PostgreSQL's planned execution strategy.

```sql
EXPLAIN
SELECT *
FROM taxi_trips
WHERE pu_location_id = 132;
```

The initial plan contained:

```text
Seq Scan on taxi_trips
```

A sequential scan means PostgreSQL plans to scan the table while checking rows against the filter condition.

---

## Understanding the Execution Plan

The initial plan included:

```text
cost=0.00..15554.00
rows=38483
width=104
```

### cost

`cost` is PostgreSQL's internal estimate used to compare possible execution strategies.

It is **not measured in milliseconds**.

### rows

PostgreSQL estimated approximately:

```text
38,483 rows
```

would match the condition.

### width

`width` represents the estimated average size of each output row in bytes.

---

## EXPLAIN ANALYZE

`EXPLAIN ANALYZE` goes further than `EXPLAIN`.

```sql
EXPLAIN ANALYZE
SELECT *
FROM taxi_trips
WHERE pu_location_id = 132;
```

Unlike plain `EXPLAIN`, `EXPLAIN ANALYZE` actually executes the query.

The Week 2 result was:

```text
Estimated rows:        38,483
Actual rows:           39,392
Rows removed:         460,608
Execution Time:       330.859 ms
```

The estimate was relatively close to the actual number of matching rows.

---

# Sequential Scan

Before indexing, PostgreSQL used:

```text
Seq Scan
```

The query returned:

```text
39,392
```

records while:

```text
460,608
```

records were removed by the filter.

Together:

```text
39,392 + 460,608 = 500,000
```

This demonstrated that the full 500,000-row table was considered during the scan.

---

# Creating an Index

An index was created on:

```text
pu_location_id
```

using:

```sql
CREATE INDEX idx_taxi_pu_location
ON taxi_trips (pu_location_id);
```

The query was then executed again using `EXPLAIN ANALYZE`.

---

# Bitmap Index Scan

After indexing, PostgreSQL selected:

```text
Bitmap Index Scan
        ↓
Bitmap Heap Scan
```

The Bitmap Index Scan used:

```text
idx_taxi_pu_location
```

to identify matching row locations.

PostgreSQL then used the Bitmap Heap Scan to retrieve the corresponding rows from the table.

The execution time was:

```text
108.358 ms
```

compared with the original:

```text
330.859 ms
```

For this particular experiment, the indexed query was approximately **3 times faster**.

Execution times can vary between runs because of factors such as caching and system activity, so these measurements represent the observed Week 2 experiment rather than a universal performance guarantee.

---

# Selectivity

Selectivity describes how much of a table satisfies a condition.

A condition matching relatively few rows is more selective.

A condition matching most of the table has low selectivity.

---

## Higher-Selectivity Example

The pickup-location query returned:

```text
39,392 / 500,000
≈ 7.9%
```

PostgreSQL chose to use the pickup-location index.

---

## Low-Selectivity Example

A second experiment examined:

```sql
WHERE payment_type = 1
```

The query returned:

```text
410,533 / 500,000
≈ 82.1%
```

of the table.

Before creating an index, PostgreSQL used:

```text
Seq Scan
```

with an observed execution time of:

```text
143.090 ms
```

---

# Index Exists but Is Not Used

An index was then created:

```sql
CREATE INDEX idx_taxi_payment_type
ON taxi_trips (payment_type);
```

The same query was executed again.

PostgreSQL still selected:

```text
Seq Scan
```

The observed execution time was:

```text
144.513 ms
```

This demonstrated one of the most important Week 2 lessons:

> Creating an index does not guarantee that PostgreSQL will use it.

Because approximately 82% of the table matched the condition, PostgreSQL estimated that scanning the table was cheaper than using the index to retrieve such a large portion of the records.

---

# Planning Time vs Execution Time

`EXPLAIN ANALYZE` also reports:

```text
Planning Time
Execution Time
```

### Planning Time

Time spent deciding how the query should be executed.

### Execution Time

Time spent actually executing the chosen plan.

These should not be confused with PostgreSQL's:

```text
cost=...
```

Planner cost is a relative estimate, while execution time is reported in milliseconds.

---

# Why Not Index Every Column?

Indexes can improve certain reads, but they also have costs.

Indexes:

- consume additional storage
- must be maintained during inserts
- must be maintained during updates
- must be maintained during deletes
- may not help low-selectivity queries

Therefore, indexes should be designed around real query patterns rather than automatically created for every column.

---

# Optimization Workflow

A useful performance-analysis workflow is:

```text
Write query
    ↓
EXPLAIN
    ↓
Understand query plan
    ↓
EXPLAIN ANALYZE
    ↓
Measure actual performance
    ↓
Identify possible optimization
    ↓
Create appropriate index
    ↓
Run same query again
    ↓
Compare execution plans and measurements
```

The important step is measuring **before and after** rather than assuming an optimization worked.

---

# Key Takeaways

- `EXPLAIN` shows PostgreSQL's planned execution strategy.
- `EXPLAIN ANALYZE` executes the query and reports actual statistics.
- `Seq Scan` scans table rows sequentially.
- Planner `cost` is not milliseconds.
- Estimated rows can be compared with actual rows.
- Indexes provide PostgreSQL with additional access strategies.
- A Bitmap Index Scan can efficiently identify many matching row locations.
- PostgreSQL does not have to use an available index.
- Selectivity strongly affects whether an index is useful.
- Low-selectivity filters may still use sequential scans.
- Performance optimization should be measured with before-and-after execution plans.