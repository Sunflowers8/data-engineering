-- ============================================================
-- WEEK 02 — SQL JOIN PRACTICE
-- Database: employee_db
-- ============================================================


-- ============================================================
-- 1. INNER JOIN
-- Goal: Show employees who have a valid department
-- Columns: name, department_name, salary
-- ============================================================

select employee_join.name,
department.department_name,
employee_join.salary
from employee_join
inner join department
ON employee_join.department_id=department.department_id;



-- ============================================================
-- 2. LEFT JOIN
-- Goal: Show every employee, including employees whose
-- department does not exist
-- Columns: name, department_name, salary
-- ============================================================
select employee_join.name,
department.department_name,
employee_join.salary
from employee_join
left join department
ON employee_join.department_id=department.department_id;



-- ============================================================
-- 3. RIGHT JOIN
-- Goal: Show every department, including departments
-- without employees
-- Columns: department_name, name
-- ============================================================

select department.department_name,
employee_join.name
from employee_join 
right join department
ON employee_join.department_id=department.department_id;


-- ============================================================
-- 4. LEFT JOIN — PRESERVE DEPARTMENTS
-- Goal: Show every department using LEFT JOIN
-- Columns: department_name, name
-- ============================================================

select department.department_name,
employee_join.name
from department 
left join employee_join
ON department.department_id=employee_join.department_id;


-- ============================================================
-- 5. FULL OUTER JOIN
-- Goal: Show all employees and all departments
-- Include unmatched records from both tables
-- Columns: name, department_name
-- ============================================================

select employee_join.name,
department.department_name
from employee_join
full outer join department
ON employee_join.department_id=department.department_id;



-- ============================================================
-- 6. JOIN + WHERE
-- Goal: Show employees with a valid department whose salary
-- is greater than 30000 and less than 50000
-- Columns: name, department_name, salary
-- ============================================================

select employee_join.name,
department.department_name,
employee_join.salary
from employee_join
inner join department
on employee_join.department_id=department.department_id
where employee_join.salary>30000 and employee_join.salary<50000;

-- ============================================================
-- 7. MULTIPLE-TABLE INNER JOIN
-- Goal: Join employee, department, and manager tables
-- Show employees who have a valid department and manager
-- Columns: employee_name, department_name, manager_name
-- ============================================================

select employee_join.name as employee_name,
department.department_name,
manager.manager_name 
from employee_join 
inner join department 
on employee_join.department_id=department.department_id
inner join manager 
on employee_join.department_id=manager.department_id;

-- ============================================================
-- 8. MULTIPLE-TABLE LEFT JOIN
-- Goal: Show every employee, including employees without
-- a matching department or manager
-- Columns: employee_name, department_name, manager_name
-- ============================================================

select employee_join.name as employee_name,
department.department_name,
manager.manager_name
from employee_join 
left join department 
on employee_join.department_id=department.department_id 
left join manager 
on department.department_id = manager.department_id ;

-- ============================================================
-- 9. MULTIPLE-TABLE JOIN — PRESERVE ALL DEPARTMENTS
-- Goal: Show every department, including departments without
-- employees or managers
-- Columns: department_name, employee_name, manager_name
-- ============================================================

select employee_join.name as employee_name,
department.department_name,
manager.manager_name
from employee_join 
right join department 
on employee_join.department_id=department.department_id 
left join manager 
on department.department_id = manager.department_id ;

-- ============================================================
-- 10. MULTIPLE-TABLE JOIN + WHERE
-- Goal: Show employees with a valid department whose salary
-- is greater than or equal to 30000
-- Include manager information when available
-- Columns: employee_name, department_name, manager_name, salary
-- ============================================================

select employee_join.name as employee_name,
department.department_name,
manager.manager_name,
employee_join.salary 
from employee_join 
inner join department 
on employee_join.department_id=department.department_id 
left join manager 
on department.department_id = manager.department_id
where employee_join.salary>=30000;
