# SQL Set Operations

## Overview

Set operations combine the results of two or more SELECT queries vertically.

Unlike JOINs, which usually combine columns from related tables, set operations combine rows returned by separate queries.

The main set operations are:

- UNION
- UNION ALL
- INTERSECT
- EXCEPT

For set operations, the SELECT statements should return the same number of columns, and corresponding columns should have compatible data types.

---

## 1. UNION

UNION combines rows from both queries and removes duplicates.

```sql
SELECT name
FROM employee_join
WHERE salary >= 30000

UNION

SELECT name
FROM employee_join
WHERE department_id = 101;
```

If the same employee appears in both queries, the employee appears only once in the final result.

### Key Idea

UNION = A OR B, with duplicates removed.

---

## 2. UNION ALL

UNION ALL combines rows from both queries and keeps duplicates.

```sql
SELECT name
FROM employee_join
WHERE salary >= 30000

UNION ALL

SELECT name
FROM employee_join
WHERE department_id = 101;
```

If Simran and Sita appear in both queries, they appear twice in the final result.

### Key Idea

UNION ALL = A OR B, including duplicates.

---

## 3. INTERSECT

INTERSECT returns rows that appear in both query results.

```sql
SELECT name
FROM employee_join
WHERE salary >= 30000

INTERSECT

SELECT name
FROM employee_join
WHERE department_id = 101;
```

Only employees satisfying both query results are returned.

### Key Idea

INTERSECT = A AND B.

---

## 4. EXCEPT

EXCEPT returns rows from the first query that do not appear in the second query.

```sql
SELECT name
FROM employee_join
WHERE salary >= 30000

EXCEPT

SELECT name
FROM employee_join
WHERE department_id = 101;
```

The order of the queries matters.

### Key Idea

EXCEPT = A MINUS B.

---

## Set Operation Comparison

| Operation | Meaning | Duplicate Handling |
|---|---|---|
| UNION | Rows from A or B | Removes duplicates |
| UNION ALL | Rows from A or B | Keeps duplicates |
| INTERSECT | Rows common to A and B | Removes duplicates |
| EXCEPT | Rows in A but not B | Removes duplicates |

---

## UNION vs JOIN

JOIN usually combines columns horizontally:

```text
name | department | manager
```

Set operations combine query results vertically:

```text
Query A
  ↓
Query B
  ↓
Combined rows
```

---

## Important Lessons

1. UNION removes duplicate rows.
2. UNION ALL keeps duplicate rows.
3. INTERSECT returns rows common to both results.
4. EXCEPT returns rows from the first result that are absent from the second.
5. Order matters with EXCEPT.
6. Both SELECT statements must return the same number of columns.
7. Corresponding columns should have compatible data types.
8. UNION ALL avoids duplicate removal when duplicate elimination is unnecessary.