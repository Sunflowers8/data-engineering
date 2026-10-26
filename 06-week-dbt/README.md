# Week 6 — dbt & Analytics Engineering

## Overview

Developed an analytics engineering project using dbt Core and DuckDB, transforming 500,000 NYC Taxi trip records into daily revenue summaries.

## Topics Covered

- dbt Core setup and DuckDB integration
- Source definitions and staging models
- SQL transformations using `source()` and `ref()`
- View and table materializations
- Built-in and custom data-quality tests
- Incremental models with merge strategy
- Incremental INSERT and UPDATE simulations
- Jinja macros and reusable SQL logic
- Model documentation and data lineage

## Project

**NYC Taxi dbt Analytics Project**

See [nyc_taxi_dbt](nyc_taxi_dbt/README.md) for the implementation, SQL models, tests, and setup instructions.

## Validation

Final practice build:

- 3 models successfully built
- 11 data-quality tests passed
- 0 warnings and 0 errors
- Incremental processing verified using a separate practice database

## Next Learning Areas

Intermediate models, source freshness, advanced testing, late-arriving data, and CI integration.