-- ============================================================
-- WEEK 02 — SUBQUERY PRACTICE
-- Database: employee_db
-- ============================================================


-- ============================================================
-- 1. SCALAR SUBQUERY WITH AVG
-- Goal: Find employees earning less than the average salary
-- Columns: name, salary
-- ============================================================

select name,
salary
from employee_join
where salary<
(
select avg(salary)
from employee_join);

-- ============================================================
-- 2. SUBQUERY WITH IN
-- Goal: Find employees belonging to Data or HR departments
-- Columns: name, department_id
-- ============================================================

select name,
department_id
from employee_join 
where department_id IN (
	select department_id
	from department 
	where department_name in ('Data','HR')
);

-- ============================================================
-- 3. SUBQUERY WITH NOT IN
-- Goal: Find employees who do not belong to Data or HR
-- Columns: name, department_id
-- ============================================================

select name,
department_id
from employee_join  
where department_id not in (
select department_id
from department
where department_name in ('Data','HR')
);

-- ============================================================
-- 4. SUBQUERY WITH EXISTS
-- Goal: Find departments that have at least one employee
-- Columns: department_name
-- ============================================================

SELECT department_name
FROM department
WHERE EXISTS (
    SELECT 1
    FROM employee_join
    WHERE employee_join.department_id = department.department_id
);

-- ============================================================
-- 5. SUBQUERY WITH NOT EXISTS
-- Goal: Find departments that have no employees
-- Columns: department_name
-- ============================================================

SELECT department_name
FROM department
WHERE not EXISTS (
    SELECT 1
    FROM employee_join
    WHERE employee_join.department_id = department.department_id
);

-- ============================================================
-- 6. CORRELATED SUBQUERY WITH EXISTS
-- Goal: Find employees whose department has a manager
-- Columns: name, department_id
-- ============================================================
 
 select name,
department_id
from employee_join
where exists (
select 1
from manager
where employee_join.department_id =manager.department_id
);