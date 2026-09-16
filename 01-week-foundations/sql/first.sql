-- ============================================================
-- WEEK 01 — SQL FOUNDATIONS
-- Database: employee_db
-- Table: employee
-- ============================================================


-- 1. VIEW ALL EMPLOYEES

SELECT *
FROM employee;


-- 2. SELECT SPECIFIC COLUMNS

SELECT name,
       department,
       salary
FROM employee;


-- 3. FILTER USING WHERE
-- Employees earning more than 30,000

SELECT name,
       department,
       salary
FROM employee
WHERE salary > 30000;


-- 4. AND CONDITION
-- Data department employees earning more than 35,000

SELECT name,
       department,
       salary
FROM employee
WHERE department = 'Data'
  AND salary > 35000;


-- 5. OR CONDITION
-- HR employees OR employees earning more than 40,000

SELECT name,
       department,
       salary
FROM employee
WHERE department = 'HR'
   OR salary > 40000;


-- 6. ORDER BY
-- Employees ordered from highest salary to lowest

SELECT name,
       department,
       salary
FROM employee
ORDER BY salary DESC;


-- 7. LIMIT
-- Top 3 highest-paid employees

SELECT name,
       salary
FROM employee
ORDER BY salary DESC
LIMIT 3;


-- 8. AGGREGATION
-- Average salary of all employees

SELECT AVG(salary) AS average_salary
FROM employee;


-- 9. GROUP BY
-- Average salary for each department

SELECT department,
       AVG(salary) AS average_salary
FROM employee
GROUP BY department;


-- ============================================================
-- WEEK 01 KEY SQL CONCEPTS
-- ============================================================

-- SELECT   = choose columns
-- FROM     = choose table
-- WHERE    = filter rows
-- AND / OR = combine conditions
-- ORDER BY = sort results
-- DESC     = descending order
-- LIMIT    = restrict number of returned rows
-- AVG()    = calculate average
-- GROUP BY = group rows before aggregation


-- Typical SQL clause order:
--
-- SELECT
-- FROM
-- WHERE
-- GROUP BY
-- HAVING
-- ORDER BY
-- LIMIT