# NYC Taxi Analytics Engineering with dbt

## Project Overview

A local analytics engineering project built with dbt Core and DuckDB using 500,000 NYC Taxi trip records.

The project transforms taxi records into analytics-ready daily revenue summaries, implements automated data-quality tests, and demonstrates incremental processing.

## Tech Stack

- Python 3.12
- dbt Core 1.12.6
- dbt-duckdb 1.11.0
- DuckDB
- SQL, Jinja, and YAML

## Data Pipeline

```text
NYC Taxi Source Data
        |
        v
stg_taxi_trips (View)
        |
        +------------------------+
        |                        |
        v                        v
daily_taxi_revenue       incremental_daily_revenue
(Table)                  (Incremental Table)
```

## Models

| Model | Materialization | Purpose |
|---|---|---|
| `stg_taxi_trips` | View | Standardizes names and data types |
| `daily_taxi_revenue` | Table | Calculates daily trip counts, total revenue, and average trip revenue |
| `incremental_daily_revenue` | Incremental | Maintains daily trip counts and total revenue using a merge strategy |

## Data Quality

The project includes 11 data-quality tests covering:

- Required pickup and dropoff timestamps
- Required daily summary values
- Unique pickup dates in daily revenue models
- A custom check for trips ending before their pickup time

## Incremental Processing

The incremental model uses `pickup_date` as its unique key and DuckDB's merge strategy.

A separate practice database was used to verify:

- Inserting a new January 8, 2026 daily summary
- Updating that day's recorded revenue from $20 to $30
- Preserving one summary row per date when the model is rerun

The model uses a limited lookback window and is not intended to capture corrections to arbitrary historical dates.

## Running the Project

Create a local dbt profile named `nyc_taxi_dbt` with a DuckDB target pointing to a database containing `main.taxi_native`.

From this project directory:

```bash
dbt debug
dbt build
dbt docs generate
dbt docs serve --port 8080
```

The local DuckDB data files and dbt connection profile are not included in the repository.

## Key Concepts Practiced

dbt models, source definitions, `ref()`, Jinja macros, staging, marts, materializations, incremental merge, idempotency, automated tests, documentation, and lineage.