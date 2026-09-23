-- ============================================================
-- NYC YELLOW TAXI SQL MINI-PROJECT
-- ============================================================


-- 1. Dataset size

SELECT COUNT(*) AS total_trips
FROM taxi_trips;


-- 2. Date range

SELECT MIN(pickup_datetime) AS earliest_pickup,
       MAX(pickup_datetime) AS latest_pickup
FROM taxi_trips;


-- 3. Average trip distance

SELECT AVG(trip_distance) AS average_trip_distance
FROM taxi_trips;


-- 4. Average trip duration

SELECT AVG(trip_duration_minutes) AS average_trip_duration
FROM taxi_trips;


-- 5. Total revenue

SELECT SUM(total_amount) AS total_revenue
FROM taxi_trips;


-- 6. Trips by payment type

SELECT payment_type,
       COUNT(*) AS total_trips
FROM taxi_trips
GROUP BY payment_type
ORDER BY total_trips DESC;


-- 7. Busiest pickup locations

SELECT pu_location_id,
       COUNT(*) AS total_pickups
FROM taxi_trips
GROUP BY pu_location_id
ORDER BY total_pickups DESC
LIMIT 10;


-- 8. Highest revenue pickup locations

SELECT pu_location_id,
       SUM(total_amount) AS total_revenue
FROM taxi_trips
GROUP BY pu_location_id
ORDER BY total_revenue DESC
LIMIT 10;


-- 9. Data-quality check: zero/negative distances

SELECT COUNT(*) AS suspicious_distance_records
FROM taxi_trips
WHERE trip_distance <= 0;


-- 10. Data-quality check: negative fares

SELECT COUNT(*) AS negative_fare_records
FROM taxi_trips
WHERE fare_amount < 0;


-- 11. Query performance before/after indexing

EXPLAIN ANALYZE
SELECT *
FROM taxi_trips
WHERE pu_location_id = 132;


-- Index created during Week 2:
-- CREATE INDEX idx_taxi_pu_location
-- ON taxi_trips (pu_location_id);


-- 12. Low-selectivity index experiment

EXPLAIN ANALYZE
SELECT *
FROM taxi_trips
WHERE payment_type = 1;


-- 13. Partition pruning

EXPLAIN
SELECT *
FROM taxi_trips_partitioned
WHERE pickup_datetime >= '2025-12-01'
  AND pickup_datetime < '2026-01-01';


-- ============================================================
-- END OF MINI-PROJECT
-- ============================================================