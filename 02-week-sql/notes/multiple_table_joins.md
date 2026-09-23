# Multiple-Table JOINs

A query can JOIN more than two related tables.

During practice, I used three tables:

```text
employee_join
      ↓ department_id
department
      ↓ department_id
manager
```

Each additional JOIN requires its own `ON` condition.

## Three-Table INNER JOIN

```sql
SELECT employee_join.name AS employee_name,
       department.department_name,
       manager.manager_name
FROM employee_join
INNER JOIN department
    ON employee_join.department_id = department.department_id
INNER JOIN manager
    ON department.department_id = manager.department_id;
```

This returns employees that have matching department and manager records.

## Preserving All Employees

To keep every employee even when department or manager information is
missing, I used LEFT JOINs:

```sql
SELECT employee_join.name AS employee_name,
       department.department_name,
       manager.manager_name
FROM employee_join
LEFT JOIN department
    ON employee_join.department_id = department.department_id
LEFT JOIN manager
    ON department.department_id = manager.department_id;
```

Employees without matching records still appear, with missing values
shown as `NULL`.

## Preserving All Departments

When the requirement is to keep every department, it is clearer to start
with the department table:

```sql
SELECT department.department_name,
       employee_join.name AS employee_name,
       manager.manager_name
FROM department
LEFT JOIN employee_join
    ON department.department_id = employee_join.department_id
LEFT JOIN manager
    ON department.department_id = manager.department_id;
```

This keeps departments even when they have no employees or managers.

## Multiple JOINs with WHERE

JOINs can also be combined with filtering:

```sql
SELECT employee_join.name AS employee_name,
       department.department_name,
       manager.manager_name,
       employee_join.salary
FROM employee_join
INNER JOIN department
    ON employee_join.department_id = department.department_id
LEFT JOIN manager
    ON department.department_id = manager.department_id
WHERE employee_join.salary >= 30000;
```

## Key Lessons

1. Multiple-table JOINs follow the same logic as two-table JOINs.
2. Every new JOIN needs an appropriate `ON` condition.
3. The table that must be preserved helps determine the JOIN type.
4. INNER JOIN removes records without a match.
5. LEFT JOIN can preserve records even when later information is missing.
6. Using `table_name.column_name` makes multi-table queries easier to understand and avoids ambiguous column names.

