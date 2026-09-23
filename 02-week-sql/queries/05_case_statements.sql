-- ============================================================
-- WEEK 02 — CASE STATEMENT PRACTICE
-- Database: employee_db
-- ============================================================


-- 1. SALARY LEVEL
-- Low / Medium / High

SELECT name,
       salary,
       CASE
           WHEN salary < 30000 THEN 'Low'
           WHEN salary BETWEEN 30000 AND 40000 THEN 'Medium'
           ELSE 'High'
       END AS salary_level
FROM employee_join;

-- 2. DEPARTMENT STATUS
-- Data Team / Finance Team / HR Team / Unknown Department

select  name,
		department_id,
		case 
			when department_id=101 then 'Data team'
			when department_id=102 then 'Finance team'
			when department_id=103 then 'HR Team'
			else 'Unknown department'
		end as department_status
from employee_join;

-- 3. MULTIPLE CONDITIONS
-- Senior Data / Data / Other

select name,
salary,
department_id,
case 
	when department_id=101 and salary > 40000 then 'Senior Data'
	when department_id=101 and salary <= 40000 then 'Data'
	else 'Other'	
end as employee_category
from employee_join;

-- 4. PERFORMANC BAND
-- Top / Standard / Entry

select name,
salary,
case
	when salary >= 45000 then 'Top'
	when salary >= 30000 and salary < 45000 then 'standard'
	when salary < 30000 then 'Entry'
end as performance_band
from employee_join;

