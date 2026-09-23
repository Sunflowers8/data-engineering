# SQL Date Functions

## Overview

Date functions are used to work with dates and timestamps in SQL.

They are important in data engineering and analytics because datasets often contain dates such as:

- Hire dates
- Transaction dates
- Order dates
- Login timestamps
- Created dates
- Updated dates

In PostgreSQL, dates can be filtered, compared, grouped, and used in calculations.

---

## Practice Data

A `hire_date` column was added to the `employee_join` table.

```sql
ALTER TABLE employee_join
ADD COLUMN hire_date DATE;
```

The employee hire dates used for practice were:

```text
Simran → 2023-01-15
Ram    → 2022-06-10
Sita   → 2024-03-20
Hari   → 2021-11-05
Gita   → 2025-07-12
```

---

## 1. CURRENT_DATE

`CURRENT_DATE` returns the current date according to the PostgreSQL session.

```sql
SELECT name,
       hire_date,
       CURRENT_DATE AS today
FROM employee_join;
```

It does not require parentheses.

```sql
CURRENT_DATE
```

can be used directly in calculations and filters.

---

## 2. EXTRACT

`EXTRACT` retrieves a specific part of a date.

Basic syntax:

```sql
EXTRACT(part FROM date_column)
```

### Extract Year

```sql
SELECT name,
       hire_date,
       EXTRACT(YEAR FROM hire_date) AS hire_year
FROM employee_join;
```

### Extract Month

```sql
SELECT name,
       hire_date,
       EXTRACT(YEAR FROM hire_date) AS hire_year,
       EXTRACT(MONTH FROM hire_date) AS hire_month
FROM employee_join;
```

Other useful date parts include:

```sql
EXTRACT(DAY FROM hire_date)
EXTRACT(MONTH FROM hire_date)
EXTRACT(YEAR FROM hire_date)
```

---

## 3. Filtering Using EXTRACT

Date parts can also be used inside a `WHERE` condition.

Example: employees hired in 2023 or later.

```sql
SELECT name,
       hire_date,
       EXTRACT(YEAR FROM hire_date) AS hire_year
FROM employee_join
WHERE EXTRACT(YEAR FROM hire_date) >= 2023;
```

A SELECT alias such as `hire_year` generally cannot be used directly in the `WHERE` clause of the same query.

Therefore, the expression is repeated:

```sql
WHERE EXTRACT(YEAR FROM hire_date) >= 2023
```

instead of:

```sql
WHERE hire_year >= 2023
```

---

## 4. Date Arithmetic

PostgreSQL allows dates to be subtracted.

```sql
CURRENT_DATE - hire_date
```

When one `DATE` is subtracted from another `DATE`, PostgreSQL returns the number of days between them.

Example:

```sql
SELECT name,
       hire_date,
       (CURRENT_DATE - hire_date) AS days_employed
FROM employee_join;
```

This can be useful for calculating:

- Days employed
- Days since registration
- Days since an order
- Days between events

---

## 5. AGE()

`AGE()` calculates the interval between two dates.

```sql
AGE(CURRENT_DATE, hire_date)
```

Example:

```sql
SELECT name,
       hire_date,
       AGE(CURRENT_DATE, hire_date) AS employment_duration
FROM employee_join;
```

Unlike simple date subtraction, `AGE()` produces a human-readable interval.

For example:

```text
3 years 8 mons 6 days
```

### Date Subtraction vs AGE

```text
CURRENT_DATE - hire_date
→ total number of days

AGE(CURRENT_DATE, hire_date)
→ years, months and days
```

---

## 6. DATE_TRUNC

`DATE_TRUNC` reduces a date or timestamp to a specified level of precision.

Example:

```sql
SELECT name,
       hire_date,
       DATE_TRUNC('month', hire_date) AS hire_month
FROM employee_join;
```

Example transformation:

```text
2023-01-15 → 2023-01-01
2024-03-20 → 2024-03-01
2025-07-12 → 2025-07-01
```

Useful levels include:

```sql
DATE_TRUNC('year', hire_date)
DATE_TRUNC('quarter', hire_date)
DATE_TRUNC('month', hire_date)
```

`DATE_TRUNC` is especially useful when aggregating data by month, quarter, or year.

---

## 7. Filtering Date Ranges with BETWEEN

`BETWEEN` can filter dates within an inclusive range.

Example: employees hired between January 1, 2023 and December 31, 2024.

```sql
SELECT name,
       hire_date
FROM employee_join
WHERE hire_date BETWEEN DATE '2023-01-01'
                    AND DATE '2024-12-31';
```

`BETWEEN` includes both boundary values.

---

## 8. DATE Literals

A date can be explicitly written using:

```sql
DATE '2023-01-01'
```

This makes it clear that the value is a date rather than ordinary text.

Example:

```sql
WHERE hire_date >= DATE '2023-01-01'
```

Explicit date literals can make SQL easier to understand and avoid data-type ambiguity.

---

## 9. Combining Date Conditions

Multiple date conditions can be combined using `AND`.

Example: employees hired in 2023 or later who have worked for more than 365 days.

```sql
SELECT name,
       hire_date,
       (CURRENT_DATE - hire_date) AS days_employed
FROM employee_join
WHERE EXTRACT(YEAR FROM hire_date) >= 2023
  AND (CURRENT_DATE - hire_date) > 365;
```

Both conditions must be true for the employee to appear.

---

## WHERE vs CASE

A useful distinction learned during date filtering:

### WHERE

`WHERE` decides which rows should appear.

```sql
WHERE hire_date BETWEEN DATE '2023-01-01'
                    AND DATE '2024-12-31'
```

### CASE

`CASE` classifies or transforms values.

```sql
CASE
    WHEN condition THEN value
    ELSE value
END
```

If the goal is to remove rows that do not satisfy a condition, use `WHERE`.

---

## AND vs UNION

Another important distinction:

### AND

Use `AND` when the same row must satisfy multiple conditions.

```sql
WHERE condition_1
  AND condition_2
```

### UNION

Use `UNION` when combining the results of separate SELECT queries.

```sql
SELECT ...
UNION
SELECT ...
```

Two conditions in one filtering requirement do not automatically require a set operation.

---

## Common Mistakes

### 1. Using a SELECT alias in WHERE

Incorrect:

```sql
SELECT
    (CURRENT_DATE - hire_date) AS days_employed
FROM employee_join
WHERE days_employed > 365;
```

Correct:

```sql
SELECT
    (CURRENT_DATE - hire_date) AS days_employed
FROM employee_join
WHERE (CURRENT_DATE - hire_date) > 365;
```

---

### 2. Reversing Comparison Operators

For:

```text
2023 or later
```

use:

```sql
>= 2023
```

not:

```sql
<= 2023
```

---

### 3. Using CASE When WHERE Is Needed

`CASE` changes or categorizes output values.

`WHERE` filters rows.

---

### 4. Using UNION for AND Logic

If an employee must satisfy two conditions simultaneously, use:

```sql
WHERE condition_1
  AND condition_2
```

not two separate queries combined with `UNION`.

---

## Key Takeaways

1. `CURRENT_DATE` returns the current date.
2. `EXTRACT` retrieves individual date components.
3. `EXTRACT(YEAR FROM date)` retrieves the year.
4. `EXTRACT(MONTH FROM date)` retrieves the month.
5. Subtracting two dates can calculate the number of days between them.
6. `AGE()` returns a human-readable interval.
7. `DATE_TRUNC()` reduces dates/timestamps to a chosen time level.
8. `BETWEEN` can filter inclusive date ranges.
9. Explicit `DATE` literals make date types clear.
10. `WHERE` filters rows while `CASE` classifies values.
11. `AND` requires multiple conditions to be true for the same row.
12. SELECT aliases generally cannot be referenced in the `WHERE` clause of the same query.
13. Date functions are essential for time-based analysis and data pipelines.