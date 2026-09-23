# Week 2 — Advanced SQL for Data Engineering

## Overview

Week 2 focuses on building practical SQL skills required for data engineering.

The goal of this week was not only to learn SQL syntax, but to understand how SQL is used to:

- combine data from multiple tables
- structure complex queries
- perform analytical calculations
- detect and remove duplicate records
- identify sessions and continuous data sequences
- update datasets safely
- preserve historical records
- analyze query execution plans
- improve query performance using indexes
- understand partitioning and partition pruning
- understand clustering concepts

The week started with small PostgreSQL practice tables and progressed to working with a real NYC Yellow Taxi dataset containing **500,000 records**.

---

## Tools Used

- PostgreSQL 16
- DBeaver
- VS Code
- SQL
- Git & GitHub
- NYC Taxi & Limousine Commission Yellow Taxi Trip Data

---

# Topics Covered

## 1. SQL Joins

Practiced combining related tables using:

- INNER JOIN
- LEFT JOIN
- RIGHT JOIN
- FULL OUTER JOIN
- JOIN with WHERE conditions
- Multiple-table joins

### Key Learning

Joins combine columns from related tables using a common key.

Example:

```sql
SELECT e.name,
       d.department_name
FROM employee_join e
INNER JOIN department d
    ON e.department_id = d.department_id;
```

An important lesson was understanding that joins may increase the number of returned rows when one record matches multiple records in another table.

---

## 2. Common Table Expressions (CTEs)

CTEs were used to create temporary named query results.

```sql
WITH high_salary AS (
    SELECT *
    FROM employee_join
    WHERE salary > 30000
)
SELECT *
FROM high_salary;
```

CTEs helped make complex SQL queries easier to read and organize.

Practiced:

- basic CTEs
- CTEs with joins
- CTEs with aggregation
- multiple CTEs

---

## 3. Subqueries

Practiced queries nested inside other queries.

Topics included:

- scalar subqueries
- `IN`
- `NOT IN`
- `EXISTS`
- `NOT EXISTS`
- correlated subqueries

Example:

```sql
SELECT name,
       department_id
FROM employee_join
WHERE EXISTS (
    SELECT 1
    FROM manager
    WHERE employee_join.department_id = manager.department_id
);
```

This helped demonstrate how SQL can test relationships without necessarily returning columns from the second table.

---

## 4. Set Operations

Learned how to combine result sets vertically.

Practiced:

- UNION
- UNION ALL
- INTERSECT
- EXCEPT

### Important Difference

`UNION` removes duplicate rows while `UNION ALL` keeps duplicates.

Also learned the difference between joins and set operations:

- JOIN combines tables horizontally through columns.
- Set operations combine compatible query results vertically through rows.

---

## 5. CASE Statements

Used `CASE` to create conditional logic inside SQL.

Example:

```sql
SELECT name,
       salary,
       CASE
           WHEN salary >= 45000 THEN 'Top'
           WHEN salary >= 30000 AND salary < 45000 THEN 'Standard'
           WHEN salary < 30000 THEN 'Entry'
       END AS performance_band
FROM employee_join;
```

Practiced:

- salary classification
- department status
- multiple conditions
- performance bands
- range-based classification

---

## 6. SQL Date Functions

Added `hire_date` to the employee dataset and practiced working with dates.

Functions and concepts included:

- CURRENT_DATE
- EXTRACT
- AGE
- DATE_TRUNC
- date arithmetic
- BETWEEN
- date filtering

Example:

```sql
SELECT name,
       hire_date,
       CURRENT_DATE - hire_date AS days_employed
FROM employee_join
WHERE EXTRACT(YEAR FROM hire_date) >= 2023
  AND CURRENT_DATE - hire_date > 365;
```

---

# 7. Window Functions

Window functions were one of the major analytical SQL topics covered this week.

Practiced:

- ROW_NUMBER()
- RANK()
- DENSE_RANK()
- PARTITION BY
- AVG() OVER()
- MAX() OVER()
- running totals
- LAG()
- LEAD()

Example:

```sql
SELECT name,
       department_id,
       salary,
       RANK() OVER (
           PARTITION BY department_id
           ORDER BY salary DESC
       ) AS department_rank,
       AVG(salary) OVER (
           PARTITION BY department_id
       ) AS department_average
FROM employee_join;
```

### Important Learning

`GROUP BY` collapses multiple rows into grouped results.

Window functions perform calculations across related rows while preserving the original rows.

---

# 8. Deduplication

A separate `employee_updates` table was created containing multiple versions of employee records.

The objective was to identify the latest record and older duplicate versions.

Example:

```sql
WITH ranked_employees AS (
    SELECT employee_id,
           name,
           salary,
           updated_at,
           ROW_NUMBER() OVER (
               PARTITION BY employee_id
               ORDER BY updated_at DESC
           ) AS row_num
    FROM employee_updates
)
SELECT *
FROM ranked_employees
WHERE row_num = 1;
```

Practiced:

- identifying duplicate records
- selecting the newest record
- identifying older versions
- counting duplicate records
- counting duplicates by employee
- identifying employees with multiple records

### Key Pattern

```text
PARTITION BY business_key
ORDER BY timestamp DESC
ROW_NUMBER()
```

This is a common data-engineering deduplication pattern.

---

# 9. Sessionization

Sessionization groups related events into sessions based on time gaps.

A 30-minute inactivity threshold was used in the practice example.

The process was:

```text
LAG()
   ↓
Calculate time gap
   ↓
CASE
   ↓
Mark new session as 1
   ↓
Running SUM()
   ↓
Session ID
```

Example pattern:

```sql
WITH event_gaps AS (
    SELECT user_id,
           event_time,
           LAG(event_time) OVER (
               PARTITION BY user_id
               ORDER BY event_time
           ) AS previous_event
    FROM website_events
),
session_flags AS (
    SELECT user_id,
           event_time,
           previous_event,
           CASE
               WHEN previous_event IS NULL THEN 1
               WHEN event_time - previous_event > INTERVAL '30 minutes' THEN 1
               ELSE 0
           END AS new_session
    FROM event_gaps
)
SELECT user_id,
       event_time,
       SUM(new_session) OVER (
           PARTITION BY user_id
           ORDER BY event_time
       ) AS session_id
FROM session_flags;
```

---

# 10. Gaps and Islands

Gaps and islands identify consecutive sequences in data.

The same general pattern used for sessionization was applied:

```text
LAG()
→ identify gap
→ CASE
→ running SUM()
→ island ID
```

This demonstrated how window functions can identify continuous groups of dates or events.

---

# 11. MERGE

Practiced synchronizing a staging table with a target table using PostgreSQL `MERGE`.

Example:

```sql
MERGE INTO employee_merge AS target
USING employee_staging AS source
ON target.employee_id = source.employee_id

WHEN MATCHED THEN
    UPDATE SET salary = source.salary

WHEN NOT MATCHED THEN
    INSERT (employee_id, name, salary)
    VALUES (
        source.employee_id,
        source.name,
        source.salary
    );
```

This allowed existing records to be updated and new records to be inserted.

---

# 12. UPSERT

PostgreSQL `ON CONFLICT` was also practiced.

```sql
INSERT INTO employee_merge (
    employee_id,
    name,
    salary
)
VALUES (
    2,
    'Ram',
    32000
)
ON CONFLICT (employee_id)
DO UPDATE
SET salary = EXCLUDED.salary;
```

### Key Difference

`MERGE` explicitly handles matched and unmatched records.

`ON CONFLICT` attempts an insert and handles a primary-key or unique-key conflict.

---

# 13. Slowly Changing Dimension Type 2

SCD Type 2 was introduced to preserve historical changes instead of overwriting old information.

Example employee history:

```text
Ram
Salary 28,000
2026-01-01 → 2026-09-22
is_current = false

Ram
Salary 32,000
2026-09-23 → NULL
is_current = true
```

A surrogate key was used:

```sql
employee_key SERIAL PRIMARY KEY
```

while `employee_id` remained the business key.

### SCD Type 2 Process

When a tracked attribute changes:

```text
1. Find current record
2. Close current record
3. Set end_date
4. Set is_current = false
5. Insert new version
6. Set is_current = true
```

If the incoming record contains no tracked changes, no new historical version is required.

---

# Real-World SQL Practice — NYC Yellow Taxi Data

After completing the SQL foundations, Week 2 moved to a real dataset.

A **500,000-row sample** of January 2026 NYC Yellow Taxi trip data was loaded into PostgreSQL.

Table:

```text
taxi_trips
```

Rows:

```text
500,000
```

The table includes fields such as:

- pickup datetime
- dropoff datetime
- pickup location
- dropoff location
- trip distance
- passenger count
- payment type
- fare amount
- tip amount
- tolls
- total amount
- trip duration

This dataset was used to practice database performance and physical data organization.

---

# 14. EXPLAIN and Query Optimization

`EXPLAIN` was used to understand how PostgreSQL planned queries.

Example:

```sql
EXPLAIN
SELECT *
FROM taxi_trips
WHERE pu_location_id = 132;
```

Initial execution plan:

```text
Seq Scan on taxi_trips
```

Using `EXPLAIN ANALYZE` showed actual execution statistics.

Before indexing:

```text
Rows returned: 39,392
Rows removed by filter: 460,608
Execution Time: 330.859 ms
```

This showed that PostgreSQL was scanning all 500,000 records to find the required rows.

### EXPLAIN vs EXPLAIN ANALYZE

`EXPLAIN` displays the planned execution strategy.

`EXPLAIN ANALYZE` actually executes the query and reports real execution statistics.

---

# 15. Indexes

An index was created on pickup location:

```sql
CREATE INDEX idx_taxi_pu_location
ON taxi_trips (pu_location_id);
```

After creating the index, PostgreSQL selected:

```text
Bitmap Index Scan
        ↓
Bitmap Heap Scan
```

Execution time changed from approximately:

```text
330.859 ms
```

to:

```text
108.358 ms
```

for that particular test.

This was approximately a **3× improvement** in the observed execution time.

---

## Index Selectivity

A second experiment used:

```sql
WHERE payment_type = 1
```

This condition matched:

```text
410,533 / 500,000 rows
≈ 82.1%
```

An index was created on `payment_type`, but PostgreSQL continued using:

```text
Seq Scan
```

Execution times were approximately:

```text
Before index: 143.090 ms
After index:  144.513 ms
```

This demonstrated an important database optimization principle:

> Creating an index does not guarantee that PostgreSQL will use it.

When a condition matches a very large percentage of the table, PostgreSQL may determine that a sequential scan is cheaper.

---

# 16. Partitioning

A partitioned version of the taxi dataset was created using:

```sql
PARTITION BY RANGE (pickup_datetime)
```

Before creating partitions, the actual timestamp range was checked:

```sql
SELECT MIN(pickup_datetime) AS earliest_pickup,
       MAX(pickup_datetime) AS latest_pickup
FROM taxi_trips;
```

Result:

```text
Earliest pickup:
2025-12-31 23:57:29

Latest pickup:
2026-01-07 17:08:32
```

This showed that the January source sample also contained several December timestamps.

Two partitions were created:

```text
taxi_trips_partitioned
│
├── taxi_trips_2025_12
│
└── taxi_trips_2026_01
```

December:

```sql
FOR VALUES FROM ('2025-12-01')
TO ('2026-01-01')
```

January:

```sql
FOR VALUES FROM ('2026-01-01')
TO ('2026-02-01')
```

The 500,000 records were then inserted into the partitioned parent table.

PostgreSQL automatically routed them:

```text
December 2025:       6 rows
January 2026:  499,994 rows
Total:         500,000 rows
```

---

# 17. Partition Pruning

Partition pruning was verified using `EXPLAIN`.

For a December-only query:

```sql
EXPLAIN
SELECT *
FROM taxi_trips_partitioned
WHERE pickup_datetime >= '2025-12-01'
  AND pickup_datetime < '2026-01-01';
```

PostgreSQL produced:

```text
Seq Scan on taxi_trips_2025_12
```

The January partition was absent from the execution plan.

This demonstrated that PostgreSQL could eliminate irrelevant partitions before scanning the data.

### Important Distinction

```text
Partition pruning
→ determines WHICH partitions need to be searched.

Sequential / Index Scan
→ determines HOW PostgreSQL searches inside those partitions.
```

A query can therefore successfully use partition pruning while still performing a sequential scan inside the selected partition.

---

# 18. Clustering Concepts

Clustering was studied conceptually alongside partitioning.

### Partitioning

Partitioning divides a large dataset into separate physical sections.

Example:

```text
Taxi trips
├── January
├── February
├── March
└── April
```

### Clustering

Clustering organizes related values closer together to improve access patterns.

For a large taxi warehouse where queries commonly filter by month and then pickup location, a sensible conceptual design would be:

```text
Partition:
pickup_datetime

Cluster / organize:
pu_location_id
```

PostgreSQL's `CLUSTER` command differs from warehouse clustering systems such as BigQuery or Snowflake. PostgreSQL can physically reorder a table using an index, but that ordering is not continuously maintained as new records are added.

---

# Week 2 Key Lessons

The most important lessons from this week were:

1. SQL joins combine related datasets.
2. CTEs and subqueries help structure complex logic.
3. Window functions enable analytics without collapsing rows.
4. `ROW_NUMBER()` is useful for deduplication and latest-record selection.
5. `LAG()` and running `SUM()` can identify sessions and islands.
6. MERGE and UPSERT synchronize incoming and existing data.
7. SCD Type 2 preserves historical changes.
8. `EXPLAIN ANALYZE` helps investigate real query performance.
9. Index usefulness depends heavily on query selectivity.
10. PostgreSQL's optimizer may intentionally ignore an available index.
11. Partitioning can divide large time-based datasets efficiently.
12. Partition pruning eliminates irrelevant partitions from a query plan.
13. Physical database design should follow real query patterns.

---

# Week 2 Checklist

- [x] INNER JOIN
- [x] LEFT JOIN
- [x] RIGHT JOIN
- [x] FULL OUTER JOIN
- [x] JOIN with WHERE conditions
- [x] Multiple-table joins
- [x] CTEs
- [x] Subqueries
- [x] Set operations
- [x] CASE statements
- [x] Date functions
- [x] Window functions
- [x] Deduplication
- [x] Sessionization
- [x] Gaps and Islands
- [x] MERGE
- [x] UPSERT
- [x] SCD Type 2
- [x] EXPLAIN
- [x] EXPLAIN ANALYZE
- [x] Query optimization
- [x] Indexes
- [x] Index selectivity
- [x] Partitioning
- [x] Partition pruning
- [x] Clustering concepts

---

## Status

**Week 2 — Advanced SQL: Completed ✅**

The next stage of the internship roadmap is **Week 3 — Python Data Pipelines**, where the focus moves from manually querying data to building reusable Python programs that extract, validate, transform, and load data.