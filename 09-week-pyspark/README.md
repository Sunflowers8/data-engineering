# Week 9 — PySpark & Distributed Data Processing

## Overview

Built a local Apache Spark analytics pipeline using PySpark
to process 500,000 NYC Yellow Taxi records.

The project demonstrates Spark DataFrames, transformations,
aggregations, Spark SQL, lazy evaluation, partitioning,
Parquet storage, and output validation.

## Technologies

- Python 3.12.7
- PySpark 4.1.1
- Java 21
- Apache Parquet

## Learning Exercises

| File | Purpose |
|------|---------|
| first_spark.py | First SparkSession and DataFrame |
| taxi_transformations.py | Select, filter, and create columns |
| taxi_aggregations.py | GroupBy and aggregation functions |
| taxi_spark_sql.py | Query DataFrames using Spark SQL |
| lazy_evaluation.py | Inspect lazy evaluation and execution plans |
| taxi_partitions.py | Explore Spark partitions and repartitioning |
| taxi_parquet.py | Write and read Parquet files |
| inspect_nyc_taxi.py | Inspect the real NYC Taxi dataset |
| nyc_taxi_pipeline.py | Complete taxi analytics pipeline |
| validate_taxi_summary.py | Validate aggregated output |

## NYC Taxi Pipeline

Source:
data/processed/nyc_taxi/taxi_sample_500k.parquet

The pipeline:

1. Reads NYC Taxi records from Parquet
2. Converts pickup datetime strings into timestamps
3. Filters records with missing or invalid values
4. Aggregates trip statistics by pickup date
5. Writes daily summaries to Parquet
6. Reads and validates the generated output

## Verified Results

- Source records: 500,000
- Valid records: 491,230
- Filtered records: 8,770
- Output summary dates: 8
- Invalid summary rows: 0
- Reconciled trip count: 491,230

## Run the Project

Activate the Week 9 environment from the repository root:

    source 09-week-pyspark/.venv/bin/activate

Run the analytics pipeline:

    python 09-week-pyspark/nyc_taxi_pipeline.py

Validate the output:

    python 09-week-pyspark/validate_taxi_summary.py

## Environment

PySpark runs locally using two worker threads and a
1 GB Spark driver memory configuration.

The Week 9 virtual environment and generated Parquet files
are excluded from Git.

The original source dataset and DuckDB warehouse are not
modified by this project.

## Limitations

This is a local learning project, not a distributed
production cluster.

The validation currently uses expected totals specific
to the existing sample dataset.

The cleaning rules exclude certain invalid or missing
values but do not cover every possible taxi data anomaly.

## Key Learning Outcomes

- Create and manage SparkSessions
- Use DataFrame transformations and actions
- Perform grouped aggregations
- Query DataFrames using Spark SQL
- Understand lazy evaluation and execution plans
- Inspect and redistribute Spark partitions
- Read and write Parquet datasets
- Build and validate a larger analytics pipeline
