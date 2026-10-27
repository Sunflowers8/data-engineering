# Week 7 — Apache Airflow & Pipeline Orchestration

## Project Overview

Built an Apache Airflow orchestration pipeline that validates, transforms, and tests 500,000 NYC Yellow Taxi records using DuckDB and dbt Core.

The project demonstrates workflow orchestration, task dependencies, manual and scheduled DAG execution, retries, data-quality validation, monitoring, and containerized deployment.

## Technologies

- Apache Airflow 3.1.7
- Python 3.12
- DuckDB 1.5.6
- dbt Core 1.12.6
- dbt-duckdb 1.11.0
- Docker, Docker Compose, and Colima

## Pipeline Architecture

NYC Taxi Data (DuckDB)
        |
        v
check_source_data
        |
        v
run_dbt_models
        |
        v
run_dbt_tests
        |
        v
confirm_pipeline_success

## DAGs

| DAG | Purpose |
|-----|---------|
| first_taxi_pipeline | Demonstrates TaskFlow dependencies and automatic retries |
| daily_taxi_schedule | Demonstrates daily scheduling at 6 AM Nepal time |
| nyc_taxi_data_check | Validates 500,000 taxi source records |
| nyc_taxi_dbt_pipeline | Orchestrates the complete DuckDB and dbt workflow |

## Data Transformation and Validation

The pipeline executes three dbt models:

1. stg_taxi_trips — staging view
2. daily_taxi_revenue — aggregated revenue table
3. incremental_daily_revenue — incremental revenue table

It then runs 11 dbt data-quality tests, covering null checks, uniqueness, and invalid trip times.

Validated results:
- Source records: 500,000
- dbt models: 3 passed
- dbt tests: 11 passed
- Airflow orchestration tasks: 4 passed
- DAG runtime: approximately 52 seconds during the verified run

## Running Locally

Prerequisites:
- Docker and Docker Compose
- At least 4 GiB allocated to the Docker runtime
- A local NYC Taxi DuckDB practice database

The expected practice database location is:

07-week-airflow/data/airflow_taxi_practice.duckdb

The database is excluded from Git and must be created separately.

From the repository root, build and start Airflow:

    docker compose -f 07-week-airflow/compose.yaml build
    docker compose -f 07-week-airflow/compose.yaml up -d

Open the Airflow dashboard at:

http://localhost:8081

Trigger the `nyc_taxi_dbt_pipeline` DAG to execute the workflow.

To stop the environment:

    docker compose -f 07-week-airflow/compose.yaml down

## Reliability and Monitoring

- Task dependencies enforce execution order.
- Retries demonstrate recovery from temporary failures.
- dbt tasks have 3-minute execution timeouts.
- DAG logs provide debugging and validation evidence.
- The primary dbt DAG limits concurrent runs.
- Airflow metadata and logs are persisted in a local runtime directory.

## Project Structure

    07-week-airflow/
    ├── Dockerfile
    ├── compose.yaml
    ├── requirements-dbt.txt
    ├── .gitignore
    ├── README.md
    ├── dags/
    │   ├── first_taxi_pipeline.py
    │   ├── daily_taxi_schedule.py
    │   ├── nyc_taxi_data_check.py
    │   └── nyc_taxi_dbt_pipeline.py
    ├── profiles/
    │   └── profiles.yml
    ├── data/                 # Ignored practice database
    └── runtime/              # Ignored metadata and logs

## Limitations

This is a local learning environment rather than a production deployment.

The pipeline uses an existing practice dataset rather than continuously ingesting new taxi files. The source count check assumes 500,000 records. Production improvements would include automated ingestion, dynamic data validation, external alerts, and a production-grade metadata database.

## Key Learning Outcomes

- Created DAGs using Airflow's TaskFlow API
- Configured task dependencies, retries, and schedules
- Understood cron expressions, logical dates, and catchup
- Integrated Airflow with DuckDB and dbt
- Built a reproducible Docker image
- Used Docker Compose for local deployment
- Monitored task logs, durations, and execution failures
- Implemented task execution timeouts
