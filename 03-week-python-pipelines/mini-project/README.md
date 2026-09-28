# NYC Taxi Data Ingestion Pipeline

## Project Overview

This mini-project demonstrates a modular Python data ingestion and transformation pipeline using the NYC Taxi Trip Records dataset.

The project was developed as part of Week 3 of my Data Engineering internship learning roadmap and focuses on practical Python pipeline development.

The pipeline demonstrates:

- Parquet data extraction
- Data transformation with Pandas
- Modular Python project structure
- Type hints and dataclass configuration
- CSV data loading
- PostgreSQL loading with SQLAlchemy
- Object-Oriented Programming (OOP)
- REST API extraction
- Retry and backoff handling
- Logging and exception handling
- Pydantic data validation
- Unit testing with pytest
- API mocking


## Dataset

Source: NYC Taxi & Limousine Commission (TLC) Yellow Taxi Trip Records.

The January 2026 Yellow Taxi dataset contains approximately 3.7 million trip records.

The raw Parquet file is kept outside Git because of its size.


## Pipeline Architecture

### NYC Taxi Pipeline

NYC TLC Parquet

        ↓

Extract

        ↓

Pandas DataFrame

        ↓

Transform

        ↓

500,000-row analytical sample

        ↓
        
CSV Output + PostgreSQL


## Pipeline Components

### Extract

`extract.py`

Reads the source Parquet dataset into a Pandas DataFrame.


### Transform

`transform.py`

Performs transformations including:

- Calculating trip duration
- Converting trip duration to minutes
- Selecting required analytical columns
- Creating a 500,000-row working sample


### Load

`load.py`

Supports loading transformed data into:

- CSV
- PostgreSQL


### Configuration

`config.py`

Uses a Python dataclass to manage:

- Input path
- Output path
- Sample size


### Database Client

`database.py`

Implements an OOP-based database client using SQLAlchemy.

The client creates and provides the database engine used by the loading layer.


## API Extraction

The project also demonstrates ingestion from a REST API.

`api_extract.py` implements an API client with:

- `requests.Session`
- HTTP timeout
- Retry handling
- Backoff
- HTTP status validation
- Exception handling
- Logging
- JSON normalization
- Pydantic validation

API data is converted from nested JSON into a Pandas DataFrame.


## Data Validation

Pydantic models are used to validate expected API fields and data types before further processing.

Example validated fields:

- `id`
- `name`
- `email`

This prevents unexpected API data from silently entering the pipeline.


## Error Handling and Reliability

The API ingestion process includes:

- Request timeout
- Retry attempts
- Backoff between retries
- HTTP error handling
- Pydantic validation errors
- Pipeline logging


## Testing

Tests are written using `pytest`.

The test suite demonstrates:

- API client creation testing
- Mock response testing
- API extraction testing
- Mocking external API calls

Mocking allows the extraction logic to be tested without depending on a live external API.


## PostgreSQL Integration

The transformed NYC Taxi data can be loaded into PostgreSQL using SQLAlchemy.

For development and learning purposes, the pipeline loads the first 100 transformed rows into:

`taxi_trips_pipeline`

The row count was verified directly in PostgreSQL.


## Project Structure

03-week-python-pipelines/
├── src/
│   ├── main.py
│   ├── inspect_taxi_data.py
│   └── pipeline/
│       ├── __init__.py
│       ├── api_extract.py
│       ├── config.py
│       ├── database.py
│       ├── extract.py
│       ├── load.py
│       └── transform.py
├── tests/
│   └── test_api_extract.py
└── mini-project/
    └── README.md


## Key Skills Demonstrated

- Python
- Pandas
- Parquet
- REST APIs
- JSON
- PostgreSQL
- SQLAlchemy
- Pydantic
- Object-Oriented Programming
- Dataclasses
- Type Hints
- Exception Handling
- Logging
- Retry / Backoff
- pytest
- Mocking
- Modular Pipeline Design


## Key Learning

This project demonstrates the transition from writing individual Python scripts to designing a modular data pipeline.

Instead of placing extraction, transformation, loading, API communication, configuration, and database logic in one file, responsibilities are separated into reusable modules.

This structure provides a foundation for later orchestration, warehouse, dbt, Airflow, Docker, Spark, and streaming work.