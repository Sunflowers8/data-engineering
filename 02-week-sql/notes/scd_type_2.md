# Slowly Changing Dimension Type 2

## Overview

Slowly Changing Dimension Type 2 (SCD Type 2) is a data warehousing technique used to preserve the history of changes to dimensional data.

A normal `UPDATE` replaces the old value.

SCD Type 2 keeps the old version and creates a new version.

---

## Example

During Week 2, Ram originally had:

```text
Employee ID: 2
Department: Finance
Salary: 28000
```

His salary later changed to:

```text
32000
```

If a normal `UPDATE` were used, the value `28000` would be lost.

With SCD Type 2, both versions are preserved.

```text
Ram | Finance | 28000 | 2026-01-01 | 2026-09-22 | false
Ram | Finance | 32000 | 2026-09-23 | NULL       | true
```

---

## Surrogate Key vs Business Key

The table used:

```sql
employee_key SERIAL PRIMARY KEY
```

and:

```sql
employee_id INT
```

These serve different purposes.

### Business Key

`employee_id` identifies the real-world employee.

Ram continues to have:

```text
employee_id = 2
```

across all historical versions.

### Surrogate Key

`employee_key` uniquely identifies each individual historical row.

Example:

```text
employee_key | employee_id
-------------|------------
1            | 2
2            | 2
```

Both records belong to Ram, but each represents a different version.

This is why `employee_id` cannot be the primary key of an SCD Type 2 table when multiple historical versions must exist.

---

## Important SCD Type 2 Columns

### start_date

Indicates when a version became valid.

### end_date

Indicates when that version stopped being valid.

The current version normally has:

```text
end_date = NULL
```

### is_current

Makes it easy to identify the current version.

```text
TRUE  → current record
FALSE → historical record
```

---

## SCD Type 2 Update Process

When a tracked attribute changes:

```text
Incoming changed record
        ↓
Find current version
        ↓
Close current version
        ↓
Set end_date
        ↓
Set is_current = FALSE
        ↓
Insert new version
        ↓
Set start_date
        ↓
end_date = NULL
        ↓
is_current = TRUE
```

---

## Step 1 — Close the Old Version

```sql
UPDATE employee_scd2
SET end_date = DATE '2026-09-22',
    is_current = FALSE
WHERE employee_id = 2
  AND is_current = TRUE;
```

The previous version becomes historical.

---

## Step 2 — Insert the New Version

```sql
INSERT INTO employee_scd2 (
    employee_id,
    name,
    department,
    salary,
    start_date,
    end_date,
    is_current
)
VALUES (
    2,
    'Ram',
    'Finance',
    32000,
    DATE '2026-09-23',
    NULL,
    TRUE
);
```

Now Ram has both a historical version and a current version.

---

## Querying Current Data

To retrieve only the current version:

```sql
SELECT *
FROM employee_scd2
WHERE employee_id = 2
  AND is_current = TRUE;
```

---

## Querying History

To see all versions:

```sql
SELECT *
FROM employee_scd2
WHERE employee_id = 2
ORDER BY start_date;
```

This allows historical analysis.

For example:

> What was this employee's salary before September 2026?

A normal overwritten table could not answer this question.

---

## What If Nothing Changed?

An important Week 2 lesson was that SCD Type 2 should not create a new version simply because another record arrives.

Suppose the current record is:

```text
Ram | Finance | 32000
```

and the incoming record is also:

```text
Ram | Finance | 32000
```

No tracked attribute changed.

Therefore:

```text
Do nothing.
```

Creating another identical historical version would produce unnecessary duplicate history.

---

## SCD Type 2 vs Normal UPDATE

### Normal UPDATE

```text
28000
   ↓
32000

Old value lost
```

### SCD Type 2

```text
28000 → historical
32000 → current

Both values preserved
```

---

## SCD Type 2 vs UPSERT

UPSERT generally asks:

```text
Does this key already exist?
```

If yes:

```text
UPDATE
```

If no:

```text
INSERT
```

This normally leaves only the latest value.

SCD Type 2 asks an additional question:

```text
Does the entity exist AND did a tracked attribute change?
```

If something changed:

```text
Close old version
+
Insert new version
```

If nothing changed:

```text
Do nothing
```

---

## SCD Type 2 vs Deduplication

Deduplication often selects one record from multiple versions:

```text
Old
Old
Latest ← select
```

SCD Type 2 intentionally preserves meaningful historical versions:

```text
Historical
Historical
Current
```

Therefore they solve different data-engineering problems.

---

## Debugging Lesson

During the Week 2 exercise, both versions temporarily appeared as current because the previous version had not been closed before inserting the new record.

The incorrect state looked conceptually like:

```text
28000 → is_current = TRUE
32000 → is_current = TRUE
```

This is inconsistent because one employee should normally have only one current version.

The old row was repaired using its surrogate `employee_key`.

This demonstrated why surrogate keys are useful when working with historical records: they allow one specific version to be targeted safely.

---

## Key Takeaways

- SCD Type 2 preserves historical changes.
- A normal `UPDATE` overwrites history.
- The business key identifies the entity.
- The surrogate key identifies each historical version.
- `start_date` records when a version becomes valid.
- `end_date` records when it stops being valid.
- `is_current` identifies the active version.
- Changed attributes require closing the old version and inserting a new one.
- Unchanged incoming records should not create unnecessary versions.
- SCD Type 2 is an important dimensional-modeling and data-warehousing concept.