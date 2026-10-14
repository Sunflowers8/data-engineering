cat >> 05-week-warehouse-storage/README.md <<'EOF'

## Study Progress — October 13, 2026

### DataCamp Courses Completed

| Course | Duration | Status |
|---|---|---|
| Data Warehousing Concepts | 4 hours | Completed |
| Introduction to Snowflake | 2 hours | Completed |

**Total:** 6 hours of DataCamp coursework.

### Practical 1: CSV vs Parquet

Using 500,000 NYC Taxi records:

| Metric | CSV | Parquet |
|---|---:|---:|
| File size | 59.40 MB | 11.11 MB |
| Selected-column read time | 0.5276 sec | 0.3489 sec |

Parquet achieved an 81.31% reduction in storage size.

### Practical 2: Partitioned Parquet

- Partition column: `pickup_date`
- Records processed: 500,000
- Date partitions created: 8
- January 1, 2026 records: 66,984
- Successfully queried data using a partition filter.

### Practical 3: External vs Native Storage

Tools: Python, PyArrow, DuckDB.

- Created a DuckDB view over partitioned Parquet files.
- Loaded the external dataset into a native DuckDB table.
- Validated that both approaches returned 66,984 January 1 records.

### Practical 4: Query Performance Benchmark

| Metric | External Parquet | Native DuckDB |
|---|---:|---:|
| Rows | 66,984 | 66,984 |
| Revenue | $1,973,735.87 | $1,973,735.87 |
| Median query time | 0.00534 sec | 0.00187 sec |

The native table was approximately 2.86 times faster in this
small, warm-cache experiment. Results are workload-dependent.

### Snowflake Concepts Studied

- Three-layer Snowflake architecture
- Storage and compute separation
- Virtual warehouses and auto-suspend
- External stages, external tables, and native tables
- COPY INTO data loading
- Micro-partitioning, clustering, and pruning
- Role-Based Access Control (RBAC)
- Least-privilege access and secrets management
- Warehouse performance and cost considerations

### Remaining Work

- Practical cloud object storage integration
- Actual Snowflake warehouse loading
- External and native table comparison in Snowflake
- Query cost analysis and optimization

**Status:** Module 5 in progress. Local exercises completed;
full cloud warehouse integration is pending.
EOF
## S3-Compatible Object Storage Practical — October 14, 2026

### Objective
Implement an object-storage pipeline using MinIO, Docker,
Python Boto3, partitioned Parquet, and DuckDB.

### Architecture
NYC Taxi CSV → Partitioned Parquet → Boto3 → MinIO → DuckDB → SQL

### Implementation
- Started MinIO using Docker and Colima.
- Created a private bucket named `nyc-taxi-data`.
- Uploaded eight date-partitioned Parquet files using Boto3.
- Verified uploaded objects using S3 HEAD requests.
- Configured DuckDB's `httpfs` extension.
- Queried Parquet directly through the S3-compatible API.
- Kept local credentials outside version control.

### Validation Results

| Metric | Result |
|---|---:|
| Parquet objects uploaded | 8 |
| Total records queried | 500,000 |
| January 1 trips | 66,984 |
| January 1 revenue | $1,973,735.87 |
| Validation | Passed |

### Engineering Lessons
- Object storage organizes files using buckets and keys.
- Hive-style date partitions can support partition pruning.
- Boto3 works with S3-compatible APIs.
- DuckDB can query object storage without importing files.
- Temporary DuckDB secrets keep credentials session-scoped.
- MinIO is a local S3-compatible alternative, not AWS S3.

### Limitations
- Local MinIO is not a production cloud deployment.
- No Snowflake external table or native Snowflake load
  has been performed.
- Actual cloud warehouse integration remains future work.
