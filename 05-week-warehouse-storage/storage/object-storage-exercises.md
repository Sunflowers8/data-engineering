# Object Storage Exercises — Week 5

## Exercise 1 — CSV vs Parquet

Converted 500,000 NYC Taxi records to Parquet.

- CSV: 59.40 MB
- Parquet: 11.11 MB
- Storage reduction: 81.31%

Script: `../src/compare_formats.py`

## Exercise 2 — Partitioned Parquet

Partitioned records using `pickup_date`.

- Total rows: 500,000
- Date partitions: 8
- January 1 rows: 66,984

Scripts:
- `../src/partition_taxi_data.py`
- `../src/read_partition.py`

## Exercise 3 — Local S3-Compatible Storage

Started MinIO using Docker and Colima.

Created private bucket: `nyc-taxi-data`.

## Exercise 4 — Object Upload

Uploaded eight Parquet objects using Boto3.

Verified uploaded file sizes with HEAD requests.

Script: `../src/upload_to_minio.py`

## Exercise 5 — Query S3-Compatible Objects

Queried Parquet files directly using DuckDB httpfs.

Results:
- Total rows: 500,000
- January 1 rows: 66,984
- January 1 revenue: $1,973,735.87

Script: `../src/query_minio.py`

## Exercise 6 — Lifecycle Policies

Studied object retention, transitions, and expiration.

Proposed retaining raw data for reprocessing and
expiring temporary exports after 90 days where permitted.

No AWS or GCS lifecycle rule was deployed.

## Key Learnings

- Buckets and object keys
- S3-compatible APIs
- Hive-style partition prefixes
- Parquet compression
- Partition filtering
- Secure credentials
- Object verification
- Lifecycle management
