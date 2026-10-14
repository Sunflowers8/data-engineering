# Week 5 — Cloud Warehouse and Object Storage Notes

## Learning Objectives

- Understand warehouse architecture and storage-compute separation.
- Compare CSV, JSON, Avro, and Parquet.
- Explain object storage, buckets, prefixes, and lifecycle policies.
- Understand partitioning, clustering, and query optimization.
- Differentiate external tables from native warehouse tables.
- Explain warehouse cost models and security principles.

## 1. Modern Data Warehouse

A data warehouse supports analytical workloads (OLAP), including
aggregations, historical analysis, and business reporting.

OLTP systems prioritize operational transactions, while OLAP
systems prioritize analytical queries.

### Warehouse vs Data Lake

| System | Purpose |
|---|---|
| Data warehouse | Structured analytical processing |
| Data lake | Store data in varied formats |
| Lakehouse | Combine lake-based storage with table management and analytical features |

## 2. Snowflake Architecture

Snowflake has three principal architectural layers:

1. Database storage — managed, compressed columnar data.
2. Compute — virtual warehouses execute workloads.
3. Cloud services — metadata, authentication, access control, and query coordination.

Storage and compute are separated.

### Virtual Warehouses

- Warehouse size affects computing capacity and credit usage.
- Auto-suspend reduces idle compute costs.
- Auto-resume restarts a suspended warehouse when needed.
- Suspending a warehouse does not delete stored data.

## 3. Storage File Formats

| Format | Characteristics | Typical Use |
|---|---|---|
| CSV | Row-oriented text, limited type information | Data exchange |
| JSON | Semi-structured, human-readable | APIs and events |
| Avro | Row-oriented binary format with schema support | Data exchange and event pipelines |
| Parquet | Columnar, compressed, supports column statistics | Analytical storage |

### Why Parquet?

Parquet allows compatible query engines to read selected columns
without processing every column in a dataset.

It supports efficient encodings and compression.

## 4. Partitioning

Partitioning organizes data by values such as dates.

Example:

    processed/pickup_date=2026-01-01/
    processed/pickup_date=2026-01-02/

A compatible query engine can prune partitions unrelated to its
filter predicate.

Excessive small partitions or files can increase overhead.

### Clustering

Clustering groups related values to make some queries more
efficient. Snowflake native tables use automatic micro-partitions,
and clustering keys may help large tables with suitable workloads.

Clustering is not always beneficial because maintenance has costs.

## 5. Object Storage

Object storage uses buckets and object keys.

Example:

    s3://nyc-taxi-data/processed/pickup_date=2026-01-01/file.parquet

- Bucket: container for objects.
- Object: data and associated metadata.
- Key: identifier within the bucket.
- Prefix: shared beginning of object keys.
- Lifecycle policy: automated object retention or transition rules.

### Lifecycle Policy Example

- Preserve raw files needed for backfills.
- Keep processed datasets according to business requirements.
- Expire temporary exports after 90 days where permitted.
- Account for retrieval costs, retention obligations, and recovery needs.

This is a proposed policy, not a deployed AWS lifecycle rule.

## 6. External and Native Tables

An external table references data outside a warehouse,
such as Parquet files in cloud object storage.

A native Snowflake table stores data managed by Snowflake.

Snowflake external stages reference files for loading and access.
COPY INTO can load supported staged files into native tables.

A local DuckDB VIEW over Parquet files demonstrated the same
external-querying concept but was not a Snowflake external table.

## 7. Query Optimization

Important techniques:

- Select only required columns.
- Apply selective filters.
- Organize partition keys around common query patterns.
- Avoid unnecessary processing.
- Compare execution plans and measured runtime.
- Use appropriate warehouse sizing and auto-suspend.

Query plans may contain estimated row counts rather than
actual rows scanned.

### Cost Models

Snowflake commonly bills warehouse compute using credits.
BigQuery supports on-demand query pricing based on data processed,
as well as capacity-based pricing.

Both platforms also have storage-related costs.

## 8. Security

- Role-Based Access Control (RBAC).
- Principle of least privilege.
- Cloud IAM and service identities.
- Secrets management and credential isolation.
- Private storage buckets.

Never commit passwords, tokens, private keys, or local credentials.

## 9. DataCamp Coursework

| Course | Duration | Result |
|---|---|---|
| Data Warehousing Concepts | 4 hours | Completed |
| Introduction to Snowflake | 2 hours | Completed |

## 10. Remaining Learning Gap

Actual integration between S3/GCS and a live Snowflake or
BigQuery warehouse has not been implemented.

This module demonstrates the principles through DataCamp
and local S3-compatible object storage.
EOF
