-- ============================================================
-- WEEK 2: EXPLAIN, QUERY OPTIMIZATION AND INDEXES
-- Dataset: 500,000 NYC Yellow Taxi trip records
-- ============================================================


-- ============================================================
-- 1. BASELINE QUERY PLAN
-- ============================================================

EXPLAIN
SELECT *
FROM taxi_trips
WHERE pu_location_id = 132;


-- Initial plan:
-- Seq Scan on taxi_trips
--
-- PostgreSQL estimated approximately 38,483 matching rows.


-- ============================================================
-- 2. MEASURE ACTUAL PERFORMANCE
-- ============================================================

EXPLAIN ANALYZE
SELECT *
FROM taxi_trips
WHERE pu_location_id = 132;


-- Actual result from Week 2:
--
-- Actual rows:            39,392
-- Rows removed by filter: 460,608
-- Execution Time:         330.859 ms
--
-- PostgreSQL examined the full 500,000-row table.


-- ============================================================
-- 3. CREATE INDEX
-- ============================================================

CREATE INDEX idx_taxi_pu_location
ON taxi_trips (pu_location_id);


-- ============================================================
-- 4. TEST THE SAME QUERY AFTER INDEXING
-- ============================================================

EXPLAIN ANALYZE
SELECT *
FROM taxi_trips
WHERE pu_location_id = 132;


-- PostgreSQL selected:
--
-- Bitmap Index Scan
--       ↓
-- Bitmap Heap Scan
--
-- Actual rows:    39,392
-- Execution Time: 108.358 ms
--
-- Observed improvement:
-- approximately 330.859 ms → 108.358 ms


-- ============================================================
-- 5. LOW-SELECTIVITY QUERY
-- ============================================================

SELECT COUNT(*)
FROM taxi_trips
WHERE payment_type = 1;


-- Result:
-- 410,533 out of 500,000 rows
-- Approximately 82.1% of the table.


EXPLAIN ANALYZE
SELECT *
FROM taxi_trips
WHERE payment_type = 1;


-- Before index:
--
-- Seq Scan
-- Actual rows: 410,533
-- Rows Removed by Filter: 89,467
-- Execution Time: 143.090 ms


-- ============================================================
-- 6. CREATE INDEX ON LOW-SELECTIVITY COLUMN
-- ============================================================

CREATE INDEX idx_taxi_payment_type
ON taxi_trips (payment_type);


-- ============================================================
-- 7. RETEST
-- ============================================================

EXPLAIN ANALYZE
SELECT *
FROM taxi_trips
WHERE payment_type = 1;


-- PostgreSQL still selected:
--
-- Seq Scan
--
-- Execution Time: 144.513 ms
--
-- The index existed, but PostgreSQL decided that scanning the
-- table was cheaper because approximately 82% of rows matched.


-- ============================================================
-- KEY LESSON
-- ============================================================

-- An index does NOT guarantee that PostgreSQL will use it.
--
-- PostgreSQL's query planner chooses the execution strategy
-- that it estimates will have the lowest cost.
--
-- Index usefulness depends on factors such as:
--
-- - selectivity
-- - number of matching rows
-- - table size
-- - query structure
-- - planner statistics
-- - cost of retrieving table pages