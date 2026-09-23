# Deduplication in SQL

## Overview

Deduplication is the process of identifying and handling multiple records that represent the same entity.

In data engineering, duplicate records commonly appear when:

- data is loaded multiple times
- the same entity is updated repeatedly
- APIs send repeated records
- multiple source systems contain the same entity
- incremental pipelines receive newer versions of existing records

During Week 2, deduplication was practiced using an `employee_updates` table containing multiple versions of the same employee.

---

# Practice Dataset

The practice table contained:

```sql
CREATE TABLE employee_updates (
    employee_id INT,
    name VARCHAR(50),
    salary DECIMAL(10,2),
    updated_at DATE
);
```

Example records:

```text
employee_id | name   | salary | updated_at
------------|--------|--------|------------
1           | Simran | 35000  | 2026-01-01
1           | Simran | 38000  | 2026-06-01
2           | Ram    | 25000  | 2026-02-01
2           | Ram    | 27000  | 2026-08-01
3           | Sita   | 45000  | 2026-03-01
```

Here:

```text
Simran → 2 records
Ram    → 2 records
Sita   → 1 record
```

The objective was to identify the newest version of each employee and distinguish it from older records.

---

# 1. Identifying Multiple Records

Before removing or filtering duplicates, we can identify entities that appear multiple times.

```sql
SELECT employee_id,
       name,
       COUNT(*) AS total_records
FROM employee_updates
GROUP BY employee_id, name
HAVING COUNT(*) > 1;
```

Expected result:

```text
Simran → 2 records
Ram    → 2 records
```

`HAVING` is used because the condition is applied after grouping.

---

# 2. Ranking Records Using ROW_NUMBER()

The main deduplication technique used during Week 2 was:

```sql
ROW_NUMBER()
```

Records were grouped by `employee_id` and ordered by `updated_at` from newest to oldest.

```sql
SELECT employee_id,
       name,
       salary,
       updated_at,

       ROW_NUMBER() OVER (
           PARTITION BY employee_id
           ORDER BY updated_at DESC
       ) AS row_num

FROM employee_updates;
```

Conceptually:

```text
employee_id | salary | updated_at | row_num
------------|--------|------------|--------
1           | 38000  | 2026-06-01 | 1
1           | 35000  | 2026-01-01 | 2

2           | 27000  | 2026-08-01 | 1
2           | 25000  | 2026-02-01 | 2

3           | 45000  | 2026-03-01 | 1
```

The most recent record receives:

```text
row_num = 1
```

Older records receive:

```text
row_num > 1
```

---

# Why PARTITION BY employee_id?

The purpose of:

```sql
PARTITION BY employee_id
```

is to restart the numbering for every employee.

Without `PARTITION BY`, PostgreSQL would number the entire table as one sequence.

With it:

```text
Employee 1
1
2

Employee 2
1
2

Employee 3
1
```

This allows each employee's records to be ranked independently.

---

# Why ORDER BY updated_at DESC?

The objective is to keep the newest record.

Therefore:

```sql
ORDER BY updated_at DESC
```

puts the most recent date first.

Example:

```text
2026-06-01 → row_num 1
2026-01-01 → row_num 2
```

This creates an important data-engineering pattern:

```text
PARTITION BY business key
+
ORDER BY update timestamp DESC
+
ROW_NUMBER()
```

---

# 3. Keeping Only the Latest Record

A CTE can first rank the records.

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

This returns only the latest version of every employee.

Expected result:

```text
Simran → 38000
Ram    → 27000
Sita   → 45000
```

---

# 4. Finding Older Duplicate Records

Instead of keeping the newest records, we can inspect the older versions.

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
WHERE row_num > 1;
```

The important condition is:

```sql
WHERE row_num > 1
```

and not simply:

```sql
WHERE row_num = 2
```

Why?

An employee could have more than two historical records.

For example:

```text
row_num = 1 → newest
row_num = 2 → older
row_num = 3 → older
row_num = 4 → older
```

Therefore:

```sql
row_num > 1
```

captures **all older versions**.

---

# 5. Counting Old Duplicate Records

We can count the total number of older records.

```sql
WITH ranked_employees AS (

    SELECT employee_id,

           ROW_NUMBER() OVER (
               PARTITION BY employee_id
               ORDER BY updated_at DESC
           ) AS row_num

    FROM employee_updates
)

SELECT COUNT(*) AS old_duplicate_records
FROM ranked_employees
WHERE row_num > 1;
```

In the Week 2 practice dataset, the result was:

```text
2
```

because Simran had one older record and Ram had one older record.

---

# 6. Counting Duplicates Per Employee

Duplicates can also be counted separately for each employee.

```sql
WITH ranked_employees AS (

    SELECT employee_id,

           ROW_NUMBER() OVER (
               PARTITION BY employee_id
               ORDER BY updated_at DESC
           ) AS row_num

    FROM employee_updates
)

SELECT employee_id,
       COUNT(*) AS duplicate_count
FROM ranked_employees
WHERE row_num > 1
GROUP BY employee_id;
```

Conceptually:

```text
employee_id | duplicate_count
------------|----------------
1           | 1
2           | 1
```

---

# Deduplication Pattern

The core Week 2 deduplication pattern was:

```text
Raw records
     ↓
PARTITION BY business key
     ↓
ORDER BY timestamp DESC
     ↓
ROW_NUMBER()
     ↓
row_num = 1
     ↓
Latest record
```

Older versions are:

```text
row_num > 1
```

---

# Business Key

A business key identifies the real-world entity represented by the records.

In the employee example:

```text
employee_id
```

was the business key.

Even though salary and update date changed, the `employee_id` continued identifying the same employee.

This is why deduplication used:

```sql
PARTITION BY employee_id
```

instead of:

```sql
PARTITION BY salary
```

or:

```sql
PARTITION BY updated_at
```

---

# Deduplication vs Removing Exact Duplicates

There are different meanings of "duplicate."

## Exact Duplicate

Two rows may be completely identical.

Example:

```text
1 | Simran | 35000
1 | Simran | 35000
```

These are exact duplicates.

---

## Multiple Versions of an Entity

Records may share the same business key but contain different information.

Example:

```text
1 | Simran | 35000 | Jan
1 | Simran | 38000 | Jun
```

These rows are not identical.

Instead, they represent different versions of the same employee.

In a data pipeline, we may want to select the newest version rather than simply applying `DISTINCT`.

---

# Why DISTINCT Is Not Enough

`DISTINCT` removes rows that are identical across the selected columns.

For example:

```sql
SELECT DISTINCT *
FROM employee_updates;
```

would not solve:

```text
Simran | 35000 | Jan
Simran | 38000 | Jun
```

because these records contain different salary and date values.

Instead, the pipeline needs business logic:

```text
Which employee?
→ employee_id

Which record is newest?
→ updated_at

Which version should be selected?
→ ROW_NUMBER() = 1
```

---

# Real Data Engineering Use

The same pattern can appear in production pipelines.

For example, an API might deliver:

```text
Customer 101
09:00 → old address
11:00 → updated address
15:00 → newest address
```

A pipeline that needs the current customer record can rank them:

```sql
ROW_NUMBER() OVER (
    PARTITION BY customer_id
    ORDER BY updated_at DESC
)
```

and keep:

```text
row_num = 1
```

This makes window-function-based deduplication a common ETL/ELT technique.

---

# Connection to SCD Type 2

Deduplication and Slowly Changing Dimension Type 2 solve different problems.

## Deduplication

Often asks:

> Which record should be considered the latest/current version?

Example:

```text
Old
Old
Current ← keep this
```

## SCD Type 2

Asks:

> How can I preserve the old versions while also identifying the current version?

Example:

```text
Historical version → preserved
Historical version → preserved
Current version    → preserved
```

Therefore:

```text
Deduplication
→ often selects the record to keep/use.

SCD Type 2
→ intentionally preserves historical versions.
```

---

# Common Deduplication Workflow

A practical data-engineering workflow can look like:

```text
Incoming data
      ↓
Identify business key
      ↓
Identify timestamp/version column
      ↓
ROW_NUMBER()
      ↓
PARTITION BY business key
      ↓
ORDER BY timestamp DESC
      ↓
Keep row_num = 1
      ↓
Clean latest dataset
```

---

# Key Takeaways

- Deduplication identifies repeated records or multiple versions of the same entity.
- A stable business key is important for identifying the entity.
- `ROW_NUMBER()` is a powerful deduplication tool.
- `PARTITION BY` separates records by entity.
- `ORDER BY updated_at DESC` puts the newest version first.
- `row_num = 1` represents the latest record.
- `row_num > 1` identifies all older versions.
- `HAVING COUNT(*) > 1` can identify entities with multiple records.
- `DISTINCT` is not sufficient when duplicate entities contain different values.
- Deduplication and SCD Type 2 serve different purposes.
- The pattern `PARTITION BY key + ORDER BY timestamp DESC + ROW_NUMBER()` is commonly used in data-engineering pipelines.