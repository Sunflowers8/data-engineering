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
 
## Object Storage Lifecycle Policy

### Proposed Retention Strategy

| Data Category | Storage Strategy | Retention |
|---|---|---|
| Raw taxi data | Frequently accessible storage | Preserve for reprocessing |
| Processed Parquet | Frequently accessible storage | According to analytical requirements |
| Temporary exports | Automatic expiration | 90 days |
| Logs | Retain or archive according to operational policy | Policy-dependent |

### Engineering Considerations

- Lifecycle policies help manage storage costs.
- Retention must consider legal and business requirements.
- Objects needed for pipeline backfills should not be deleted prematurely.
- Storage transitions can introduce retrieval costs and delays.
- MinIO is being used locally for S3-compatible API practice.
- This policy is documented as a proposal, not deployed to AWS.

## Week 5 — Final Review and Assessment

### Query Optimization Practical
Compared DuckDB execution plans with and without a date filter.

| Query | Estimated Rows | Scan Type |
|---|---:|---|
| Without date filter | ~500,000 | Sequential scan |
| With date filter | ~71,429 | Sequential scan with date filter |

The filtered plan applied `pickup_date = '2026-01-01'`
during the scan.

These are optimizer estimates, not actual scan counts.
The actual January 1 record count was 66,984.

### Object Storage Lifecycle Policies
Studied lifecycle rules for managing storage retention,
archiving, and expiration.

Proposed strategies:
- Preserve raw data required for reprocessing.
- Retain processed Parquet according to business needs.
- Expire temporary exports after 90 days.
- Consider retrieval costs and legal retention requirements.

No cloud lifecycle policy was deployed.

### Security and Cost Optimization
- Snowflake auto-suspend and auto-resume.
- Virtual warehouse sizing and compute costs.
- Partition pruning and clustering.
- BigQuery bytes-processed pricing concepts.
- Role-Based Access Control (RBAC).
- Least-privilege permissions and secrets management.

### Final Viva Assessment
Practice assessment score: 17/20 (85%).

Topics assessed:
1. Parquet partitioning and query optimization.
2. External versus native Snowflake tables.
3. Virtual warehouse auto-suspend.
4. Pipeline idempotency.

Improvement area:
Implement idempotent loads using partition replacement
or MERGE with stable unique keys.

### Module Completion Summary
Status: Local coursework and practical assessment completed.

Completed:
- CSV versus Parquet comparison.
- Partitioned Parquet processing.
- Local S3-compatible storage using MinIO and Boto3.
- Direct object-storage querying with DuckDB.
- External-versus-native database comparison.
- Query benchmarking and execution-plan inspection.
- DataCamp warehousing and Snowflake fundamentals.

Limitation:
Actual S3/GCS-to-Snowflake or BigQuery integration was
not performed. The official cloud warehouse loading
outcome remains pending.
