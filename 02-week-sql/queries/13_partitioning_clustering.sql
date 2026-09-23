-- ============================================================
-- WEEK 2: PARTITIONING AND CLUSTERING
-- Dataset: 500,000 NYC Yellow Taxi trip records
-- ============================================================


-- ============================================================
-- 1. CHECK ACTUAL DATE RANGE
-- ============================================================

SELECT MIN(pickup_datetime) AS earliest_pickup,
       MAX(pickup_datetime) AS latest_pickup
FROM taxi_trips;

-- Week 2 result:
--
-- Earliest: 2025-12-31 23:57:29
-- Latest:   2026-01-07 17:08:32
--
-- Even though the source file represented January 2026,
-- the sample contained several December 2025 timestamps.


-- ============================================================
-- 2. CREATE PARTITIONED PARENT TABLE
-- ============================================================

CREATE TABLE taxi_trips_partitioned
(
    LIKE taxi_trips INCLUDING ALL
)
PARTITION BY RANGE (pickup_datetime);


-- The new table initially contains no data.

SELECT COUNT(*)
FROM taxi_trips_partitioned;

-- Expected before loading:
-- 0


-- ============================================================
-- 3. CREATE DECEMBER 2025 PARTITION
-- ============================================================

CREATE TABLE taxi_trips_2025_12
PARTITION OF taxi_trips_partitioned
FOR VALUES FROM ('2025-12-01')
TO ('2026-01-01');


-- ============================================================
-- 4. CREATE JANUARY 2026 PARTITION
-- ============================================================

CREATE TABLE taxi_trips_2026_01
PARTITION OF taxi_trips_partitioned
FOR VALUES FROM ('2026-01-01')
TO ('2026-02-01');


-- Partition boundaries:
--
-- FROM = inclusive
-- TO   = exclusive
--
-- January therefore means:
--
-- >= 2026-01-01
-- <  2026-02-01


-- ============================================================
-- 5. LOAD EXISTING DATA INTO PARTITIONED TABLE
-- ============================================================

INSERT INTO taxi_trips_partitioned
SELECT *
FROM taxi_trips;


-- PostgreSQL automatically routes records to the correct
-- partition according to pickup_datetime.


-- ============================================================
-- 6. VERIFY TOTAL RECORDS
-- ============================================================

SELECT COUNT(*)
FROM taxi_trips_partitioned;

-- Week 2 result:
-- 500000


-- ============================================================
-- 7. VERIFY INDIVIDUAL PARTITIONS
-- ============================================================

SELECT COUNT(*)
FROM taxi_trips_2025_12;

-- Result:
-- 6


SELECT COUNT(*)
FROM taxi_trips_2026_01;

-- Result:
-- 499994


-- Total:
--
-- 6 + 499994 = 500000


-- ============================================================
-- 8. TEST PARTITION PRUNING
-- ============================================================

EXPLAIN
SELECT *
FROM taxi_trips_partitioned
WHERE pickup_datetime >= '2025-12-01'
  AND pickup_datetime < '2026-01-01';


-- Week 2 execution plan:
--
-- Seq Scan on taxi_trips_2025_12
--
-- PostgreSQL did NOT include taxi_trips_2026_01
-- in the execution plan.
--
-- This demonstrates partition pruning.


-- ============================================================
-- PARTITIONING VS SCAN TYPE
-- ============================================================

-- Partition pruning determines:
--
-- WHICH partitions PostgreSQL needs to search.
--
-- Seq Scan / Index Scan determines:
--
-- HOW PostgreSQL searches inside the selected partition.
--
-- Therefore a query can successfully use partition pruning
-- while still using a sequential scan inside a partition.


-- ============================================================
-- CLUSTERING CONCEPT
-- ============================================================

-- For a large taxi warehouse where queries commonly:
--
-- 1. filter by pickup date/month
-- 2. then filter/group by pickup location
--
-- a sensible conceptual warehouse design could be:
--
-- Partition by:
-- pickup_datetime
--
-- Cluster / organize by:
-- pu_location_id
--
-- NOTE:
-- PostgreSQL CLUSTER differs from clustering in cloud
-- warehouses such as BigQuery or Snowflake.
--
-- PostgreSQL CLUSTER physically reorganizes a table according
-- to an index, but that physical ordering is not automatically
-- maintained as new rows are inserted.