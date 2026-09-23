-- ============================================================
-- WEEK 2: SLOWLY CHANGING DIMENSION TYPE 2
-- ============================================================

-- SCD Type 2 preserves historical versions of records.

CREATE TABLE employee_scd2 (
    employee_key SERIAL PRIMARY KEY,
    employee_id INT,
    name VARCHAR(50),
    department VARCHAR(50),
    salary NUMERIC(10,2),
    start_date DATE,
    end_date DATE,
    is_current BOOLEAN
);


-- ============================================================
-- 1. INSERT INITIAL CURRENT RECORD
-- ============================================================

INSERT INTO employee_scd2 (
    employee_id,
    name,
    department,
    salary,
    start_date,
    end_date,
    is_current
)
VALUES (
    2,
    'Ram',
    'Finance',
    28000,
    DATE '2026-01-01',
    NULL,
    TRUE
);


-- ============================================================
-- 2. ATTRIBUTE CHANGE OCCURS
-- Ram's salary changes from 28000 to 32000
-- ============================================================

-- Close the previous version

UPDATE employee_scd2
SET end_date = DATE '2026-09-22',
    is_current = FALSE
WHERE employee_id = 2
  AND is_current = TRUE;


-- Insert the new current version

INSERT INTO employee_scd2 (
    employee_id,
    name,
    department,
    salary,
    start_date,
    end_date,
    is_current
)
VALUES (
    2,
    'Ram',
    'Finance',
    32000,
    DATE '2026-09-23',
    NULL,
    TRUE
);


-- ============================================================
-- 3. VIEW COMPLETE HISTORY
-- ============================================================

SELECT *
FROM employee_scd2
WHERE employee_id = 2
ORDER BY start_date;


-- ============================================================
-- 4. VIEW ONLY CURRENT RECORD
-- ============================================================

SELECT *
FROM employee_scd2
WHERE employee_id = 2
  AND is_current = TRUE;


-- ============================================================
-- EXPECTED HISTORY
-- ============================================================

-- Old version:
-- salary     = 28000
-- start_date = 2026-01-01
-- end_date   = 2026-09-22
-- is_current = false
--
-- New version:
-- salary     = 32000
-- start_date = 2026-09-23
-- end_date   = NULL
-- is_current = true


-- IMPORTANT:
-- A new SCD Type 2 version should only be created when
-- a tracked attribute actually changes.
--
-- If the incoming record is identical to the current record,
-- no historical version needs to be created.