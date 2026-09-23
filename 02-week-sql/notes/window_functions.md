# SQL Window Functions

## Overview

Window functions perform calculations across a group of related rows while keeping each individual row in the result.

Unlike `GROUP BY`, which usually combines multiple rows into fewer result rows, window functions allow us to calculate rankings, averages, totals, previous values, and next values without losing the original rows.

Window functions are widely used in data engineering and analytics for:

- Ranking records
- Finding top records within groups
- Running totals
- Comparing rows with group averages
- Finding previous and next values
- Deduplication
- Time-series analysis

---

## Basic Syntax

A window function generally follows this structure:

```sql
FUNCTION(column) OVER (
    PARTITION BY column
    ORDER BY column
)
```

The `OVER()` clause defines the window of rows used by the function.

`PARTITION BY` divides rows into groups.

`ORDER BY` determines the order of rows inside the window.

Not every window function requires both.

---

# 1. ROW_NUMBER()

`ROW_NUMBER()` assigns a unique sequential number to each row.

Example:

```sql
SELECT name,
       salary,
       ROW_NUMBER() OVER (
           ORDER BY salary DESC
       ) AS salary_position
FROM employee_join;
```

Example result:

```text
Gita    50000    1
Sita    45000    2
Simran  35000    3
Hari    30000    4
Ram     25000    5
```

Even when two rows contain the same value, `ROW_NUMBER()` still assigns different numbers.

---

# 2. RANK()

`RANK()` assigns rankings based on the specified ordering.

When multiple rows have the same value, they receive the same rank.

The next rank is skipped.

Example:

```sql
SELECT name,
       salary,
       RANK() OVER (
           ORDER BY salary DESC
       ) AS salary_rank
FROM employee_join;
```

Example with duplicate salaries:

```text
Salary    Rank

50000      1
45000      2
45000      2
35000      4
```

Because two employees share rank `2`, rank `3` is skipped.

---

# 3. DENSE_RANK()

`DENSE_RANK()` is similar to `RANK()`.

The difference is that it does not skip ranking numbers after ties.

```sql
SELECT name,
       salary,
       DENSE_RANK() OVER (
           ORDER BY salary DESC
       ) AS salary_dense_rank
FROM employee_join;
```

Example:

```text
Salary    Dense Rank

50000        1
45000        2
45000        2
35000        3
```

---

## ROW_NUMBER vs RANK vs DENSE_RANK

```text
Salary    ROW_NUMBER    RANK    DENSE_RANK

50000          1          1          1
45000          2          2          2
45000          3          2          2
35000          4          4          3
```

### ROW_NUMBER()

Always produces unique sequential numbers.

### RANK()

Tied values receive the same rank, and the next rank is skipped.

### DENSE_RANK()

Tied values receive the same rank, but no rank numbers are skipped.

---

# 4. PARTITION BY

`PARTITION BY` divides rows into groups before applying a window function.

For example, employees can be ranked separately inside each department.

```sql
SELECT name,
       department_id,
       salary,
       ROW_NUMBER() OVER (
           PARTITION BY department_id
           ORDER BY salary DESC
       ) AS department_salary_position
FROM employee_join;
```

For department `101`:

```text
Sita     101    45000    1
Simran   101    35000    2
```

The numbering restarts when PostgreSQL moves to another department.

---

# 5. Aggregate Functions as Window Functions

Aggregate functions such as:

```sql
AVG()
SUM()
MAX()
MIN()
COUNT()
```

can also be used as window functions.

The important difference is the use of `OVER()`.

Normal aggregate:

```sql
AVG(salary)
```

Window aggregate:

```sql
AVG(salary) OVER ()
```

---

# 6. Overall Average Salary

The overall average salary can be displayed beside every employee.

```sql
SELECT name,
       salary,
       AVG(salary) OVER () AS average_salary
FROM employee_join;
```

The average salary in the practice data was:

```text
37000
```

Each employee remains a separate row.

---

# 7. Department Average Salary

`PARTITION BY` can calculate an average separately for each department.

```sql
SELECT name,
       department_id,
       salary,
       AVG(salary) OVER (
           PARTITION BY department_id
       ) AS department_average
FROM employee_join;
```

For department `101`:

```text
Simran    101    35000    40000
Sita      101    45000    40000
```

The calculation is:

```text
(35000 + 45000) / 2 = 40000
```

---

# 8. Running Total

A running total accumulates values as PostgreSQL moves through ordered rows.

```sql
SELECT name,
       salary,
       SUM(salary) OVER (
           ORDER BY salary
       ) AS running_salary_total
FROM employee_join;
```

Example:

```text
Ram       25000     25000
Hari      30000     55000
Simran    35000     90000
Sita      45000    135000
Gita      50000    185000
```

The running total continuously increases as rows are processed according to the window ordering.

---

# 9. Running Total by Department

A running total can restart for each department by using `PARTITION BY`.

```sql
SELECT name,
       department_id,
       salary,
       SUM(salary) OVER (
           PARTITION BY department_id
           ORDER BY salary
       ) AS department_running_salary_total
FROM employee_join;
```

For department `101`:

```text
Simran    101    35000    35000
Sita      101    45000    80000
```

When another department begins, the running total starts again for that partition.

---

# 10. Comparing Salary with Department Average

Window functions can be used inside calculations.

```sql
SELECT name,
       department_id,
       salary,
       AVG(salary) OVER (
           PARTITION BY department_id
       ) AS department_average,
       salary - AVG(salary) OVER (
           PARTITION BY department_id
       ) AS salary_difference
FROM employee_join;
```

For department `101`:

```text
Simran    35000    40000    -5000
Sita      45000    40000     5000
```

A negative difference means the salary is below the department average.

A positive difference means it is above the department average.

---

# 11. Department Maximum Salary

`MAX()` can also be used as a window function.

```sql
SELECT name,
       department_id,
       salary,
       MAX(salary) OVER (
           PARTITION BY department_id
       ) AS department_max_salary,
       salary - MAX(salary) OVER (
           PARTITION BY department_id
       ) AS difference_from_max
FROM employee_join;
```

For department `101`:

```text
Simran    101    35000    45000    -10000
Sita      101    45000    45000         0
```

This keeps every employee while comparing their salary with the maximum salary in their department.

---

# 12. LAG()

`LAG()` retrieves a value from a previous row in the window.

```sql
SELECT name,
       salary,
       LAG(salary) OVER (
           ORDER BY salary
       ) AS previous_salary
FROM employee_join;
```

Example:

```text
Ram       25000    NULL
Hari      30000    25000
Simran    35000    30000
Sita      45000    35000
Gita      50000    45000
```

The first row returns `NULL` because there is no previous row.

---

# 13. Difference from Previous Row

`LAG()` can also be used inside calculations.

```sql
SELECT name,
       salary,
       LAG(salary) OVER (
           ORDER BY salary
       ) AS previous_salary,
       salary - LAG(salary) OVER (
           ORDER BY salary
       ) AS salary_difference
FROM employee_join;
```

Example:

```text
Ram       25000    NULL     NULL
Hari      30000    25000     5000
Simran    35000    30000     5000
Sita      45000    35000    10000
Gita      50000    45000     5000
```

---

# 14. LEAD()

`LEAD()` retrieves a value from the next row.

```sql
SELECT name,
       salary,
       LEAD(salary) OVER (
           ORDER BY salary
       ) AS next_salary
FROM employee_join;
```

Example:

```text
Ram       25000    30000
Hari      30000    35000
Simran    35000    45000
Sita      45000    50000
Gita      50000    NULL
```

The final row returns `NULL` because there is no next row.

---

# 15. LAG and LEAD Together

Previous and next values can be displayed together.

```sql
SELECT name,
       salary,
       LAG(salary) OVER (
           ORDER BY salary
       ) AS previous_salary,
       LEAD(salary) OVER (
           ORDER BY salary
       ) AS next_salary
FROM employee_join;
```

This is useful for comparing records sequentially.

---

# 16. Combining Multiple Window Functions

Multiple window calculations can be performed in the same query.

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
       ) AS department_average,
       salary - AVG(salary) OVER (
           PARTITION BY department_id
       ) AS difference_from_average
FROM employee_join;
```

This query simultaneously:

1. Ranks employees inside their departments.
2. Calculates each department's average salary.
3. Calculates the difference between employee salary and department average.

---

# GROUP BY vs Window Functions

`GROUP BY` normally reduces multiple rows into aggregated results.

Example:

```sql
SELECT department_id,
       AVG(salary)
FROM employee_join
GROUP BY department_id;
```

This returns one row per department.

A window function:

```sql
AVG(salary) OVER (
    PARTITION BY department_id
)
```

keeps every employee row while adding the department average.

This distinction is extremely important when deciding whether to use aggregation or window functions.

---

# ORDER BY Inside OVER()

The `ORDER BY` inside a window definition controls how the window function processes rows.

Example:

```sql
ROW_NUMBER() OVER (
    ORDER BY salary DESC
)
```

Here, salary determines the numbering order.

It is different from an `ORDER BY` placed at the end of the entire SQL query, which controls the final presentation order.

---

# PARTITION BY vs ORDER BY

## PARTITION BY

Answers:

> Which group does this row belong to?

Example:

```sql
PARTITION BY department_id
```

## ORDER BY

Answers:

> In what order should rows inside the window be processed?

Example:

```sql
ORDER BY salary DESC
```

They can be combined:

```sql
RANK() OVER (
    PARTITION BY department_id
    ORDER BY salary DESC
)
```

---

# Common Mistakes

## 1. Using ORDER BY When Calculating a Whole-Group Average

For the complete department average:

```sql
AVG(salary) OVER (
    PARTITION BY department_id
)
```

Adding `ORDER BY salary` changes the window behavior and may produce an ordered/running calculation instead of the intended whole-partition average.

---

## 2. Putting Calculations Inside OVER()

Incorrect idea:

```sql
AVG(salary) OVER (
    PARTITION BY department_id
    salary - AVG(salary)
)
```

`OVER()` defines the window.

The subtraction belongs outside:

```sql
salary - AVG(salary) OVER (
    PARTITION BY department_id
)
```

---

## 3. Confusing ROW_NUMBER and RANK

`ROW_NUMBER()` always assigns unique numbers.

`RANK()` allows tied values to share a rank.

Use the function that matches the requirement.

---

## 4. Forgetting DESC

```sql
ORDER BY salary
```

defaults to ascending order.

For highest salary first:

```sql
ORDER BY salary DESC
```

---

# Key Takeaways

1. Window functions calculate across related rows without collapsing them.
2. `OVER()` defines the window used by a window function.
3. `PARTITION BY` separates rows into independent groups.
4. `ORDER BY` determines processing order within a window.
5. `ROW_NUMBER()` assigns unique sequential numbers.
6. `RANK()` allows ties and skips subsequent rank numbers.
7. `DENSE_RANK()` allows ties without skipping rank numbers.
8. Aggregate functions such as `AVG()`, `SUM()`, and `MAX()` can be used with `OVER()`.
9. `SUM() OVER (ORDER BY ...)` can create running totals.
10. `LAG()` accesses a previous row.
11. `LEAD()` accesses a following row.
12. Window functions can be combined with arithmetic calculations.
13. Window functions are especially useful for ranking, comparisons, running calculations, deduplication, and analytical pipelines.