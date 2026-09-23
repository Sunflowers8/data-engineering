# SQL CASE Statements

## Overview

A `CASE` statement is used to apply conditional logic in SQL.

It works similarly to `if`, `elif`, and `else` statements in Python.

A CASE statement checks conditions in order and returns a value when a condition is true.

---

## Basic Syntax

```sql
CASE
    WHEN condition THEN result
    WHEN condition THEN result
    ELSE result
END AS column_name
```

The main keywords are:

- `CASE` — starts the conditional logic
- `WHEN` — defines a condition
- `THEN` — defines the result when the condition is true
- `ELSE` — defines the result when no previous condition matches
- `END` — closes the CASE statement
- `AS` — gives the calculated column a name

---

## 1. Salary Classification

CASE can be used to classify numerical values into categories.

Example:

```sql
SELECT name,
       salary,
       CASE
           WHEN salary < 30000 THEN 'Low'
           WHEN salary BETWEEN 30000 AND 40000 THEN 'Medium'
           ELSE 'High'
       END AS salary_level
FROM employee_join;
```

This creates a new calculated column called `salary_level`.

The rules are:

```text
salary < 30000            → Low
salary 30000 to 40000     → Medium
salary > 40000            → High
```

---

## 2. Using BETWEEN in CASE

`BETWEEN` can be useful when checking whether a value falls within a range.

```sql
WHEN salary BETWEEN 30000 AND 40000 THEN 'Medium'
```

`BETWEEN` includes both boundary values.

Therefore:

```text
30000 → included
35000 → included
40000 → included
```

It is equivalent to:

```sql
WHEN salary >= 30000 AND salary <= 40000 THEN 'Medium'
```

---

## 3. Department Classification

CASE can also convert codes or IDs into meaningful categories.

```sql
SELECT name,
       department_id,
       CASE
           WHEN department_id = 101 THEN 'Data Team'
           WHEN department_id = 102 THEN 'Finance Team'
           WHEN department_id = 103 THEN 'HR Team'
           ELSE 'Unknown Department'
       END AS department_status
FROM employee_join;
```

The `ELSE` condition handles department IDs that are not included in the defined rules.

For example:

```text
101 → Data Team
102 → Finance Team
103 → HR Team
999 → Unknown Department
```

---

## 4. CASE with Multiple Conditions

Multiple conditions can be combined using logical operators such as `AND`.

Example:

```sql
SELECT name,
       salary,
       department_id,
       CASE
           WHEN department_id = 101
                AND salary > 40000
                THEN 'Senior Data'

           WHEN department_id = 101
                AND salary <= 40000
                THEN 'Data'

           ELSE 'Other'
       END AS employee_category
FROM employee_join;
```

This checks both the employee's department and salary before assigning a category.

---

## 5. Performance Band

CASE can be used to create business categories from numerical values.

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

The classifications are:

```text
salary >= 45000             → Top
salary >= 30000 and < 45000 → Standard
salary < 30000              → Entry
```

---

## Order of WHEN Conditions

SQL evaluates `WHEN` conditions from top to bottom.

Once a condition is true, SQL returns its result and does not continue checking the remaining conditions for that CASE expression.

For this reason, the order of conditions can be important.

Example:

```sql
CASE
    WHEN salary >= 45000 THEN 'Top'
    WHEN salary >= 30000 THEN 'Standard'
    ELSE 'Entry'
END
```

A salary of `50000` matches the first condition and is classified as `Top`.

---

## Boundary Conditions

Careful handling of boundaries is important when writing CASE statements.

For example:

```sql
WHEN salary > 30000 AND salary < 40000 THEN 'Medium'
```

does NOT include:

```text
30000
40000
```

If both boundaries should be included, use:

```sql
WHEN salary >= 30000 AND salary <= 40000 THEN 'Medium'
```

or:

```sql
WHEN salary BETWEEN 30000 AND 40000 THEN 'Medium'
```

Always check values that are exactly equal to the boundaries.

---

## ELSE and NULL

`ELSE` provides a result when none of the `WHEN` conditions match.

Example:

```sql
CASE
    WHEN department_id = 101 THEN 'Data'
    WHEN department_id = 102 THEN 'Finance'
    ELSE 'Other'
END
```

If `ELSE` is omitted and no condition matches, the CASE expression returns `NULL`.

Using `ELSE` is therefore useful when every row should receive a category.

---

## CASE vs Python Conditions

Python:

```python
if salary < 30000:
    level = "Low"
elif salary <= 40000:
    level = "Medium"
else:
    level = "High"
```

SQL:

```sql
CASE
    WHEN salary < 30000 THEN 'Low'
    WHEN salary <= 40000 THEN 'Medium'
    ELSE 'High'
END
```

Both perform conditional decision-making.

---

## Common Mistakes

### 1. Missing boundary values

Incorrect:

```sql
WHEN salary > 30000 AND salary < 40000 THEN 'Medium'
```

If `30000` should also be Medium, the condition needs to include it.

---

### 2. Leaving gaps between conditions

For example:

```sql
WHEN salary >= 45000 THEN 'Top'
WHEN salary >= 30000 AND salary < 40000 THEN 'Standard'
WHEN salary < 30000 THEN 'Entry'
```

This leaves salaries from `40000` to `44999` without a matching condition.

---

### 3. Forgetting END

Every CASE expression must end with:

```sql
END
```

---

### 4. Forgetting ELSE

`ELSE` is optional, but without it unmatched rows return `NULL`.

---

## Key Takeaways

1. `CASE` adds conditional decision-making to SQL.
2. `WHEN` defines a condition.
3. `THEN` defines the result for a matching condition.
4. `ELSE` handles values that do not match previous conditions.
5. `END` closes the CASE expression.
6. `AS` can give the calculated column a meaningful name.
7. `AND` can combine multiple conditions.
8. `BETWEEN` includes both boundary values.
9. `WHEN` conditions are evaluated in order.
10. Boundary values should always be checked carefully.
11. Missing ranges can cause unexpected `NULL` values.
12. CASE statements are useful for classification, labeling, reporting, and business rules.