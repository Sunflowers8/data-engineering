-- ============================================================
-- WEEK 02 — CTE PRACTICE
-- Database: employee_db
-- ============================================================


-- ============================================================
-- 1. BASIC CTE
-- Goal: Create a temporary result containing employees
-- who belong to department 101
-- Columns: department_id, salary, name
-- ============================================================
with data_employees as (
select employee_join.department_id,
employee_join.salary,
employee_join.name
from employee_join
where employee_join.department_id=101)
select *
from data_employees;



-- ============================================================
-- 2. CTE + JOIN
-- Goal: Find employees earning more than 30000 and join
-- the temporary result with the department table
-- Columns: name, salary, department_name
-- ============================================================


with high_salary_employee as (
select employee_join.name,
employee_join.salary,
employee_join.department_id
from employee_join
where salary > 30000
)
SELECT high_salary_employee.name,
       high_salary_employee.salary,
       department.department_name
from high_salary_employee 
inner join department 
on high_salary_employee.department_id=department.department_id ;



-- ============================================================
-- 3. CTE + AGGREGATION
-- Goal: Calculate the average employee salary using a CTE
-- and find employees earning above the average salary
-- Columns: name, salary
-- ============================================================

with avg_salary as (
select avg(employee_join.salary) as avg_salary
from employee_join)
select employee_join.name,
employee_join.salary
from employee_join, 
avg_salary 
where employee_join.salary>avg_salary;


-- ============================================================
-- 4. MULTIPLE CTEs
-- Goal: Create one CTE for employees earning more than 30000
-- and another CTE for department 101, then join them
-- Columns: name, salary, department_name
-- ===========================================================

with high_salary_employees as (
select name,
salary, 
department_id
from employee_join
where salary>30000),
data_department as (
select department_id,
department_name
from department 
where department_id=101) 
select high_salary_employees.name,
high_salary_employees.salary,
data_department.department_name
from high_salary_employees
inner join data_department
on high_salary_employees.department_id=data_department.department_id;
