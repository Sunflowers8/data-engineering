# Warehouse and Query Exercises — Week 5

## Exercise 1 — External vs Native Storage

Used DuckDB to create:

1. An external view over Parquet files.
2. A native DuckDB table loaded from the external view.

Both returned 66,984 January 1 records.

Script: `../src/external_vs_native.py`

## Exercise 2 — Performance Benchmark

| Metric | External Parquet | Native DuckDB |
|---|---:|---:|
| Rows | 66,984 | 66,984 |
| Revenue | $1,973,735.87 | $1,973,735.87 |
| Median execution | 0.00534 sec | 0.00187 sec |

Native DuckDB was approximately 2.86 times faster in
this small, warm-cache experiment.

Script: `../src/benchmark_storage.py`

## Exercise 3 — Query Optimization

Studied DuckDB EXPLAIN plans.

Without date filter:
- Sequential scan
- Approximately 500,000 estimated rows

With date filter:
- Sequential scan with `pickup_date` filter
- Approximately 71,429 estimated rows

These are optimizer estimates, not actual scanned rows.

Script: `../src/query_optimization.py`

## Exercise 4 — Snowflake Concepts

Studied:
- Storage and compute separation
- Virtual warehouses
- Auto-suspend and auto-resume
- Internal and external stages
- External and native tables
- COPY INTO loading
- Micro-partitioning and clustering
- RBAC and least privilege

Snowflake was studied through DataCamp rather than
a personal cloud warehouse.

## Exercise 5 — Cost Optimization

Compared:
- Snowflake warehouse compute costs
- BigQuery on-demand bytes-processed pricing
- Storage retention considerations
- Partition pruning and selective column reads

## Final Viva Assessment

Practice score: 17/20 (85%).

| Topic | Score |
|---|---:|
| Partitioning | 4.5/5 |
| External vs native | 4/5 |
| Auto-suspend | 5/5 |
| Idempotency | 3.5/5 |

Improvement area: Implement idempotent data loading
through partition replacement or stable-key MERGE logic.

## Remaining Requirement

Actual S3/GCS-to-Snowflake or BigQuery integration
has not been performed.
