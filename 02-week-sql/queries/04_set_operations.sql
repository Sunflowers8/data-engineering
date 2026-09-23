-- ============================================================
-- WEEK 02 — SET OPERATIONS PRACTICE
-- Database: employee_db
-- ============================================================


-- ============================================================
-- 1. UNION
-- Combine two result sets and remove duplicates
-- ============================================================

select employee_join.name
from employee_join
where employee_join.salary>=30000
union
select employee_join.name 
from employee_join 
where employee_join.department_id=101;

-- ============================================================
-- 2. UNION ALL
-- Combine two result sets and keep duplicates
-- ============================================================

select employee_join.name
from employee_join
where employee_join.salary>=30000
union all
select employee_join.name 
from employee_join 
where employee_join.department_id=101;

-- ============================================================
-- 3. INTERSECT
-- Return rows appearing in both result sets
-- ============================================================

select employee_join.name
from employee_join
where employee_join.salary>=30000
intersect
select employee_join.name 
from employee_join 
where employee_join.department_id=101;

-- ============================================================
-- 4. EXCEPT
-- Return rows from the first query that are not in the second
-- ============================================================

select employee_join.name
from employee_join
where employee_join.salary>=30000
except 
select employee_join.name 
from employee_join 
where employee_join.department_id=101;

-- ============================================================
-- 5. INDEPENDENT PRACTICE
-- Employees with salary < 35000 OR department_id = 101
-- without duplicate names
-- ============================================================

select employee_join.name
from employee_join
where employee_join.salary<35000
union
select employee_join.name 
from employee_join 
where employee_join.department_id=101;