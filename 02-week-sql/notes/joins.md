# SQL JOINs

## Overview

SQL JOINs are used to combine data from two or more related tables.

In this week's practice, I worked with two tables:

### employee_join

| Column | Description |
|---|---|
| employee_id | Unique employee ID |
| name | Employee name |
| department_id | Department assigned to the employee |
| salary | Employee salary |

### department

| Column | Description |
|---|---|
| department_id | Unique department ID |
| department_name | Name of the department |

The relationship between the tables is:

```text
employee_join.department_id
            =
department.department_id
```

---

# 1. INNER JOIN

An `INNER JOIN` returns only records that have a matching value in both
tables.

```sql
SELECT employee_join.name,
       department.department_name,
       employee_join.salary
FROM employee_join
INNER JOIN department
    ON employee_join.department_id = department.department_id;
```

### What happens?

If an employee has a `department_id` that does not exist in the
`department` table, that employee is excluded.

### Memory

```text
INNER JOIN = Matching records only
```

---

# 2. LEFT JOIN

A `LEFT JOIN` keeps every record from the left table and adds matching
information from the right table.

```sql
SELECT employee_join.name,
       department.department_name
FROM employee_join
LEFT JOIN department
    ON employee_join.department_id = department.department_id;
```

If an employee does not have a matching department, the employee still
appears, but the department information becomes `NULL`.

### Memory

```text
LEFT JOIN = Keep everything from the LEFT
```

---

# 3. RIGHT JOIN

A `RIGHT JOIN` keeps every record from the right table and adds matching
information from the left table.

```sql
SELECT department.department_name,
       employee_join.name
FROM employee_join
RIGHT JOIN department
    ON employee_join.department_id = department.department_id;
```

If a department has no employee, the department still appears and the
employee information becomes `NULL`.

### Memory

```text
RIGHT JOIN = Keep everything from the RIGHT
```

---

# 4. FULL OUTER JOIN

A `FULL OUTER JOIN` keeps all records from both tables.

```sql
SELECT employee_join.name,
       department.department_name
FROM employee_join
FULL OUTER JOIN department
    ON employee_join.department_id = department.department_id;
```

This includes:

- Matching employees and departments
- Employees without a matching department
- Departments without matching employees

### Memory

```text
FULL OUTER JOIN = Keep everything from BOTH
```

---

# JOIN Comparison

| JOIN Type | What It Keeps |
|---|---|
| INNER JOIN | Matching records only |
| LEFT JOIN | All left records + matching right records |
| RIGHT JOIN | All right records + matching left records |
| FULL OUTER JOIN | All records from both tables |

A useful question before choosing a JOIN is:

> Which table's records must remain even when there is no match?

---

# Understanding NULL After a JOIN

During practice, an employee had:

```text
department_id = 999
```

but department `999` did not exist.

With an `INNER JOIN`, the employee was excluded.

With a `LEFT JOIN`, the employee remained but:

```text
department_name = NULL
```

This does **not** mean that the employee's `department_id` is NULL.

The ID is still `999`; there is simply no matching department record.

---

# One-to-Many JOIN Results

A JOIN does not always return the same number of rows as either table.

For example, if two employees belong to the Data department:

```text
Data → Simran
Data → Sita
```

the Data department appears twice in the JOIN result.

This happens because one department can match multiple employees.

---

# Choosing the Correct JOIN Key

The columns in the `ON` condition must represent the same relationship.

### Incorrect

```sql
ON department.department_id = employee_join.employee_id
```

`department_id` and `employee_id` represent different things.

### Correct

```sql
ON department.department_id = employee_join.department_id
```

Both columns represent the employee's department.

---

# JOIN with WHERE

JOINs can also be combined with filters.

Example: employees who have a valid department and earn more than 30,000
but less than 50,000:

```sql
SELECT employee_join.name,
       department.department_name,
       employee_join.salary
FROM employee_join
INNER JOIN department
    ON employee_join.department_id = department.department_id
WHERE employee_join.salary > 30000
  AND employee_join.salary < 50000;
```

---

# SQL Clause Order

A JOIN comes before the `WHERE` clause.

```text
SELECT
FROM
JOIN
ON
WHERE
GROUP BY
HAVING
ORDER BY
LIMIT
```

Example structure:

```sql
SELECT ...
FROM table1
INNER JOIN table2
    ON table1.key = table2.key
WHERE condition;
```

---

# Common Mistakes I Made

## Forgetting ON

Incorrect:

```sql
FROM employee_join
INNER JOIN department
employee_join.department_id = department.department_id
```

Correct:

```sql
FROM employee_join
INNER JOIN department
    ON employee_join.department_id = department.department_id
```

---

## Using OUTER JOIN Instead of FULL OUTER JOIN

Incorrect:

```sql
OUTER JOIN department
```

Correct:

```sql
FULL OUTER JOIN department
```

---

## Joining the Wrong IDs

Incorrect:

```sql
department.department_id = employee_join.employee_id
```

Correct:

```sql
department.department_id = employee_join.department_id
```

---

## Putting WHERE Before JOIN

Incorrect order:

```text
FROM
WHERE
JOIN
```

Correct order:

```text
FROM
JOIN
ON
WHERE
```

---

# Key Takeaways

1. JOINs combine related tables.
2. `ON` defines the relationship between the tables.
3. INNER JOIN keeps matching records only.
4. LEFT JOIN preserves the left table.
5. RIGHT JOIN preserves the right table.
6. FULL OUTER JOIN preserves both tables.
7. Unmatched values from the other table appear as `NULL`.
8. JOIN keys should represent the same relationship.
9. One record can match multiple records.
10. JOINs can be combined with `WHERE` conditions.
11. `JOIN ... ON` comes before `WHERE`.

---

