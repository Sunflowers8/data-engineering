-- ============================================================
-- WEEK 2: MERGE AND UPSERT
-- ============================================================

-- Target table
CREATE TABLE employee_merge (
    employee_id INT PRIMARY KEY,
    name VARCHAR(50),
    salary NUMERIC(10,2)
);

INSERT INTO employee_merge
VALUES
    (1, 'Simran', 35000),
    (2, 'Ram', 25000),
    (3, 'Sita', 45000);


-- Staging table containing incoming data
CREATE TABLE employee_staging (
    employee_id INT,
    name VARCHAR(50),
    salary NUMERIC(10,2)
);

INSERT INTO employee_staging
VALUES
    (2, 'Ram', 28000),
    (4, 'Gita', 40000);


-- ============================================================
-- 1. MERGE
-- ============================================================

MERGE INTO employee_merge AS target
USING employee_staging AS source
ON target.employee_id = source.employee_id

WHEN MATCHED THEN
    UPDATE SET salary = source.salary

WHEN NOT MATCHED THEN
    INSERT (employee_id, name, salary)
    VALUES (
        source.employee_id,
        source.name,
        source.salary
    );


-- Check result
SELECT *
FROM employee_merge
ORDER BY employee_id;


-- ============================================================
-- 2. UPSERT USING ON CONFLICT
-- ============================================================

INSERT INTO employee_merge (
    employee_id,
    name,
    salary
)
VALUES (
    2,
    'Ram',
    32000
)
ON CONFLICT (employee_id)
DO UPDATE
SET salary = EXCLUDED.salary;


-- Check result
SELECT *
FROM employee_merge
ORDER BY employee_id;