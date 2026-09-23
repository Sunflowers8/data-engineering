-- ============================================================
-- WEEK 2: WINDOW FUNCTIONS
-- ============================================================

-- 1. ROW_NUMBER
SELECT name,
       department_id,
       salary,
       ROW_NUMBER() OVER (
           ORDER BY salary DESC
       ) AS row_number
FROM employee_join;


-- 2. RANK
SELECT name,
       salary,
       RANK() OVER (
           ORDER BY salary DESC
       ) AS salary_rank
FROM employee_join;


-- 3. DENSE_RANK
SELECT name,
       salary,
       DENSE_RANK() OVER (
           ORDER BY salary DESC
       ) AS salary_rank
FROM employee_join;


-- 4. Rank employees inside each department
SELECT name,
       department_id,
       salary,
       RANK() OVER (
           PARTITION BY department_id
           ORDER BY salary DESC
       ) AS department_rank
FROM employee_join;


-- 5. Department average without collapsing rows
SELECT name,
       department_id,
       salary,
       AVG(salary) OVER (
           PARTITION BY department_id
       ) AS department_average
FROM employee_join;


-- 6. Compare salary with department average
SELECT name,
       department_id,
       salary,
       AVG(salary) OVER (
           PARTITION BY department_id
       ) AS department_average,
       salary - AVG(salary) OVER (
           PARTITION BY department_id
       ) AS difference_from_average
FROM employee_join;


-- 7. Running total
SELECT name,
       salary,
       SUM(salary) OVER (
           ORDER BY salary
       ) AS running_total
FROM employee_join;


-- 8. Running total within department
SELECT name,
       department_id,
       salary,
       SUM(salary) OVER (
           PARTITION BY department_id
           ORDER BY salary
       ) AS department_running_total
FROM employee_join;


-- 9. Maximum salary within department
SELECT name,
       department_id,
       salary,
       MAX(salary) OVER (
           PARTITION BY department_id
       ) AS department_max_salary
FROM employee_join;


-- 10. Previous salary using LAG
SELECT name,
       salary,
       LAG(salary) OVER (
           ORDER BY salary
       ) AS previous_salary
FROM employee_join;


-- 11. Next salary using LEAD
SELECT name,
       salary,
       LEAD(salary) OVER (
           ORDER BY salary
       ) AS next_salary
FROM employee_join;


-- 12. Final Week 2 window-function challenge
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