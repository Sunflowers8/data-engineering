-- ============================================================
-- WEEK 2: DEDUPLICATION
-- ============================================================

-- Practice table containing multiple versions of employees
CREATE TABLE employee_updates (
    employee_id INT,
    name VARCHAR(50),
    salary DECIMAL(10,2),
    updated_at DATE
);

INSERT INTO employee_updates
VALUES
    (1, 'Simran', 35000, '2026-01-01'),
    (1, 'Simran', 38000, '2026-06-01'),
    (2, 'Ram', 25000, '2026-02-01'),
    (2, 'Ram', 27000, '2026-08-01'),
    (3, 'Sita', 45000, '2026-03-01');


-- 1. Rank records from newest to oldest for each employee
SELECT employee_id,
       name,
       salary,
       updated_at,
       ROW_NUMBER() OVER (
           PARTITION BY employee_id
           ORDER BY updated_at DESC
       ) AS row_num
FROM employee_updates;


-- 2. Keep only the latest record for each employee
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


-- 3. Find old duplicate versions
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
WHERE row_num > 1;


-- 4. Count all old duplicate records
WITH ranked_employees AS (
    SELECT employee_id,
           ROW_NUMBER() OVER (
               PARTITION BY employee_id
               ORDER BY updated_at DESC
           ) AS row_num
    FROM employee_updates
)
SELECT COUNT(*) AS old_duplicate_records
FROM ranked_employees
WHERE row_num > 1;


-- 5. Count old duplicates for each employee
WITH ranked_employees AS (
    SELECT employee_id,
           ROW_NUMBER() OVER (
               PARTITION BY employee_id
               ORDER BY updated_at DESC
           ) AS row_num
    FROM employee_updates
)
SELECT employee_id,
       COUNT(*) AS duplicate_count
FROM ranked_employees
WHERE row_num > 1
GROUP BY employee_id;


-- 6. Find employees that have multiple records
SELECT employee_id,
       name,
       COUNT(*) AS total_records
FROM employee_updates
GROUP BY employee_id, name
HAVING COUNT(*) > 1;