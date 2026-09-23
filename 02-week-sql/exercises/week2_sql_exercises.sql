-- ============================================================
-- WEEK 2 SQL EXERCISES
-- Completed practice exercises
-- ============================================================


-- ============================================================
-- 1. JOINS
-- ============================================================

-- Match employees with their departments
SELECT e.name,
       d.department_name,
       e.salary
FROM employee_join e
INNER JOIN department d
ON e.department_id = d.department_id;


-- Keep every employee, including employees without
-- a matching department
SELECT e.name,
       d.department_name,
       e.salary
FROM employee_join e
LEFT JOIN department d
ON e.department_id = d.department_id;


-- Keep all records from both tables
SELECT e.name,
       d.department_name
FROM employee_join e
FULL OUTER JOIN department d
ON e.department_id = d.department_id;


-- ============================================================
-- 2. CTE
-- ============================================================

WITH high_salary AS (
    SELECT *
    FROM employee_join
    WHERE salary > 30000
)

SELECT *
FROM high_salary;


-- ============================================================
-- 3. SUBQUERY / EXISTS
-- ============================================================

-- Employees whose department has a manager

SELECT name,
       department_id
FROM employee_join
WHERE EXISTS (
    SELECT 1
    FROM manager
    WHERE employee_join.department_id = manager.department_id
);


-- ============================================================
-- 4. SET OPERATIONS
-- ============================================================

-- Employees earning below 35000 OR belonging to department 101

SELECT name
FROM employee_join
WHERE salary < 35000

UNION

SELECT name
FROM employee_join
WHERE department_id = 101;


-- ============================================================
-- 5. CASE
-- ============================================================

SELECT name,
       salary,
       CASE
           WHEN salary >= 45000 THEN 'Top'
           WHEN salary >= 30000 AND salary < 45000 THEN 'Standard'
           WHEN salary < 30000 THEN 'Entry'
       END AS performance_band
FROM employee_join;


-- ============================================================
-- 6. DATE FUNCTIONS
-- ============================================================

SELECT name,
       hire_date,
       CURRENT_DATE - hire_date AS days_employed
FROM employee_join
WHERE EXTRACT(YEAR FROM hire_date) >= 2023
  AND CURRENT_DATE - hire_date > 365;


-- ============================================================
-- 7. WINDOW FUNCTIONS
-- ============================================================

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


-- ============================================================
-- 8. DEDUPLICATION
-- ============================================================

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


-- ============================================================
-- 9. FIND EMPLOYEES WITH MULTIPLE RECORDS
-- ============================================================

SELECT employee_id,
       name,
       COUNT(*) AS total_records
FROM employee_updates
GROUP BY employee_id, name
HAVING COUNT(*) > 1;


-- ============================================================
-- 10. SCD TYPE 2 - CURRENT VERSION
-- ============================================================

SELECT *
FROM employee_scd2
WHERE is_current = TRUE;