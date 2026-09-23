# NYC Yellow Taxi SQL Analytics & Optimization Mini-Project

## Project Overview

This mini-project applies the SQL concepts learned during Week 2 to a real-world dataset.

The project uses NYC Yellow Taxi Trip Record data and focuses on SQL analytics, data quality investigation, query optimization, indexing and partitioning.

## Dataset

Source: NYC Taxi & Limousine Commission Yellow Taxi Trip Records

Original dataset:

- 3,724,889 rows
- 20 original columns
- Parquet format

For PostgreSQL practice, a sample of:

- 500,000 rows
- 21 columns

was loaded into the `taxi_trips` table.

The additional column was:

`trip_duration_minutes`

## Data Quality Investigation

The dataset was inspected before analysis.

Findings included:

- 1,088,058 missing values in several related fields in the full dataset
- the same records shared the missing-value pattern
- those records were associated with `payment_type = 0`
- 125,738 trips had distance less than or equal to zero
- 39,463 records had negative fare amounts
- one record had pickup time later than dropoff time
- 45,069 records had identical pickup and dropoff timestamps
- no exact duplicate rows were found

The suspicious records were investigated rather than automatically deleted.

## PostgreSQL

A 500,000-row sample was loaded into PostgreSQL.

Main table:

`taxi_trips`

The table contains trip timestamps, pickup/dropoff locations, passenger information, payment information, fares and trip duration.

## Query Optimization Experiment

A query filtering:

`pu_location_id = 132`

was tested using `EXPLAIN ANALYZE`.

Before indexing:

- Sequential Scan
- 39,392 rows returned
- 460,608 rows removed by filter
- Execution time: 330.859 ms

An index was created on:

`pu_location_id`

After indexing:

- Bitmap Index Scan
- Bitmap Heap Scan
- Execution time: 108.358 ms

For this test, execution time decreased substantially.

## Index Selectivity Experiment

A second query filtered:

`payment_type = 1`

It returned:

410,533 of 500,000 rows.

An index was created on `payment_type`, but PostgreSQL continued using a sequential scan.

This demonstrated that an available index is not necessarily the cheapest execution strategy when a condition matches a large percentage of a table.

## Partitioning

A range-partitioned version of the taxi table was created using:

`pickup_datetime`

Actual sample date range:

- earliest: 2025-12-31 23:57:29
- latest: 2026-01-07 17:08:32

Partitions:

- December 2025
- January 2026

After loading:

- December partition: 6 rows
- January partition: 499,994 rows
- total: 500,000 rows

## Partition Pruning

A December-only query was inspected with `EXPLAIN`.

PostgreSQL accessed only the December partition.

The January partition was excluded from the plan, demonstrating partition pruning.

## Skills Demonstrated

- PostgreSQL
- SQL analytics
- real-world dataset exploration
- data quality investigation
- EXPLAIN
- EXPLAIN ANALYZE
- query plans
- indexing
- index selectivity
- range partitioning
- partition pruning
- performance comparison

## Key Learning

This project demonstrated that data engineering is not only about writing SQL queries.

It also requires understanding data quality, database design, query execution and performance trade-offs.