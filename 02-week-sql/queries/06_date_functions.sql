-- ============================================================
-- WEEK 02 — DATE FUNCTIONS PRACTICE
-- Database: employee_db
-- ============================================================


-- 1. CURRENT_DATE

select name,
hire_date,
current_date as today
from employee_join ej;

-- 2. EXTRACT YEAR

select name,
hire_date,
extract(year from hire_date) as hire_year
from employee_join;

-- 3. EXTRACT YEAR AND MONTH

select name,
hire_date,
extract(year from hire_date) as hire_year,
extract (month from hire_date) as hire_month
from employee_join;

-- 4. FILTER BY YEAR

select name,
hire_date,
extract(year from hire_date) as hire_year 
from employee_join
where extract (year from hire_date) >= 2023 ;

-- 5. DATE ARITHMETIC — DAYS EMPLOYED

select name,
hire_date,
(current_date-hire_date) as days_employed
from employee_join;

-- 6. AGE — EMPLOYMENT DURATION

select name,
hire_date,
age(current_date,hire_date) as employment_duration
from employee_join;

-- 7. DATE_TRUNC — HIRE MONTH

select name,
hire_date,
date_trunc('month',hire_date) as hire_month
from employee_join ;

-- 8. BETWEEN — DATE RANGE FILTER

select name,
hire_date
from employee_join
where hire_date between '2023-01-01' and '2024-12-31';

-- 9. MULTIPLE DATE CONDITIONS
-- Hired in 2023 or later AND employed for more than 365 days

select name,
hire_date,
(current_date-hire_date) as days_employed
from employee_join
where extract (year from hire_date) >= 2023 
and 
(current_date-hire_date) > 365;