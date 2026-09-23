# SQL Subqueries

## What is a Subquery?

A subquery is a SQL query written inside another SQL query.

The inner query performs one part of the task, and its result is used by the outer query.

Basic structure:

```sql
SELECT ...
FROM ...
WHERE column = (
    SELECT ...
    FROM ...
);
```

A useful way to understand a subquery is:

```text
Inner query runs
       ↓
Produces a result
       ↓
Outer query uses that result
```

---

# 1. Scalar Subquery

A scalar subquery returns a single value.

Example: find employees earning less than the average salary.

```sql
SELECT name,
       salary
FROM employee_join
WHERE salary < (
    SELECT AVG(salary)
    FROM employee_join
);
```

The inner query calculates the average salary first.

The outer query then compares each employee's salary with that value.

---

# 2. Subquery with IN

`IN` is useful when a subquery returns multiple values.

Example: find employees belonging to Data or HR.

```sql
SELECT name,
       department_id
FROM employee_join
WHERE department_id IN (
    SELECT department_id
    FROM department
    WHERE department_name IN ('Data', 'HR')
);
```

The inner query returns the department IDs for Data and HR.

The outer query keeps employees whose department ID appears in that result.

---

# 3. Subquery with NOT IN

`NOT IN` excludes values returned by a subquery.

```sql
SELECT name,
       department_id
FROM employee_join
WHERE department_id NOT IN (
    SELECT department_id
    FROM department
    WHERE department_name IN ('Data', 'HR')
);
```

This returns employees whose department IDs are not Data or HR.

---

# 4. EXISTS

`EXISTS` checks whether at least one matching row exists.

```sql
SELECT department_name
FROM department
WHERE EXISTS (
    SELECT 1
    FROM employee_join
    WHERE employee_join.department_id = department.department_id
);
```

`EXISTS` does not need the actual value returned by the inner query.

It only checks:

```text
Does a matching row exist?

YES → keep the row
NO  → exclude the row
```

`SELECT 1` is commonly used because the actual selected value is not
important for `EXISTS`.

---

# 5. NOT EXISTS

`NOT EXISTS` checks that no matching row exists.

Example: find departments that have no employees.

```sql
SELECT department_name
FROM department
WHERE NOT EXISTS (
    SELECT 1
    FROM employee_join
    WHERE employee_join.department_id = department.department_id
);
```

---

# 6. Correlated Subquery

A correlated subquery refers to a value from the outer query.

Example: find employees whose department has a manager.

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

For each employee, PostgreSQL checks whether a manager exists with the
same department ID.

---

# IN vs EXISTS

| Operator | Main Question |
|---|---|
| IN | Is this value in the returned set of values? |
| NOT IN | Is this value not in the returned set? |
| EXISTS | Does at least one matching row exist? |
| NOT EXISTS | Does no matching row exist? |

---

# CTE vs Subquery

Both CTEs and subqueries can break a SQL problem into smaller steps.

A CTE gives an intermediate result a name:

```sql
WITH example AS (
    SELECT ...
)
SELECT ...
FROM example;
```

A subquery can be written directly inside another query:

```sql
SELECT ...
FROM ...
WHERE column > (
    SELECT ...
);
```

CTEs are often easier to read when a query contains several steps, while
subqueries can be convenient for smaller intermediate calculations or
conditions.

---

# Important Lessons

1. A subquery is a query inside another query.
2. The inner query can return one value or multiple values.
3. Scalar subqueries return a single value.
4. `IN` can compare a value against multiple values returned by a subquery.
5. `NOT IN` excludes values returned by a subquery.
6. `EXISTS` checks whether a matching row exists.
7. `NOT EXISTS` checks whether no matching row exists.
8. A correlated subquery references a value from the outer query.
9. Columns being compared should represent compatible values.
10. Correct relationship keys are important when using correlated subqueries.