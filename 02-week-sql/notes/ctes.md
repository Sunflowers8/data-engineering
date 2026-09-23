# Common Table Expressions (CTEs)

## What is a CTE?

A Common Table Expression (CTE) is a temporary named result that can be used within a single SQL statement.

A CTE is created using the `WITH` keyword.

Basic structure:

```sql
WITH cte_name AS (
    SELECT ...
    FROM ...
)
SELECT *
FROM cte_name;
```

A CTE does not permanently create a table in the database. It exists only while the SQL statement is being executed.

---

# Why Use CTEs?

CTEs help break complex SQL queries into smaller and more understandable steps.

Instead of writing one large query, I can:

```text
Step 1 → Prepare or filter data
Step 2 → Give the result a temporary name
Step 3 → Use that result in another query
```

CTEs are useful for filtering, JOINs, aggregations, multiple transformations, deduplication, and other data engineering tasks.

---

# 1. Basic CTE

Example: find employees from department 101.

```sql
WITH data_employees AS (
    SELECT department_id,
           salary,
           name
    FROM employee_join
    WHERE department_id = 101
)
SELECT *
FROM data_employees;
```

Here, `data_employees` is the temporary result.

---

# 2. CTE with JOIN

A CTE can be joined with another table.

```sql
WITH high_salary_employee AS (
    SELECT name,
           salary,
           department_id
    FROM employee_join
    WHERE salary > 30000
)
SELECT high_salary_employee.name,
       high_salary_employee.salary,
       department.department_name
FROM high_salary_employee
INNER JOIN department
    ON high_salary_employee.department_id = department.department_id;
```

The CTE first filters employees.

The final query then joins the filtered result with the department table.

---

# 3. CTE with Aggregation

A CTE can store a calculated value such as an average.

```sql
WITH average_salary AS (
    SELECT AVG(salary) AS avg_salary
    FROM employee_join
)
SELECT employee_join.name,
       employee_join.salary
FROM employee_join,
     average_salary
WHERE employee_join.salary > average_salary.avg_salary;
```

In this example:

```text
Average salary = 37000
```

The query then finds employees earning more than the calculated average.

---

# 4. Multiple CTEs

More than one CTE can be created in the same SQL statement.

`WITH` is written once, and the CTEs are separated using commas.

```sql
WITH high_salary_employees AS (
    SELECT name,
           salary,
           department_id
    FROM employee_join
    WHERE salary > 30000
),
data_department AS (
    SELECT department_id,
           department_name
    FROM department
    WHERE department_id = 101
)
SELECT high_salary_employees.name,
       high_salary_employees.salary,
       data_department.department_name
FROM high_salary_employees
INNER JOIN data_department
    ON high_salary_employees.department_id =
       data_department.department_id;
```

This query creates two temporary results and then joins them together.

---

# Important CTE Rule

A CTE exists only for the SQL statement immediately following it.

This works:

```sql
WITH data_employees AS (
    SELECT *
    FROM employee_join
)
SELECT *
FROM data_employees;
```

Running this separately later will not work:

```sql
SELECT *
FROM data_employees;
```

The CTE no longer exists after the original statement finishes.

---

# CTE vs Permanent Table

| CTE | Permanent Table |
|---|---|
| Temporary result | Stored in database |
| Exists for one SQL statement | Remains until changed or deleted |
| Created with `WITH` | Created with `CREATE TABLE` |
| Useful for organizing a query | Useful for permanently storing data |

---

# Key Lessons

1. A CTE is created using `WITH`.
2. A CTE gives a temporary result a name.
3. The CTE can be referenced by the main query.
4. A CTE exists only for one SQL statement.
5. CTEs can contain filtering and aggregations.
6. CTEs can be joined with regular tables.
7. Multiple CTEs can be used in one query.
8. Multiple CTEs are separated by commas.
9. `WITH` is written only once when defining multiple CTEs.
10. CTEs make complex SQL easier to organize and understand.