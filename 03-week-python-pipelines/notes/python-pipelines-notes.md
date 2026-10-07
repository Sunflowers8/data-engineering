# Week 3 — Python Data Pipelines Notes

## 1. Data Pipeline

A data pipeline moves data from a source to a destination while extracting, transforming, validating, and loading the data.

Basic ETL flow:

```text
Source → Extract → Transform → Load → Destination
```

Example from this week's work:

```text
NYC Taxi Data → Pandas → Transform/Clean → PostgreSQL
```

---

## 2. ETL

ETL stands for:

- **Extract** — retrieve data from a source.
- **Transform** — clean, validate, calculate, or restructure the data.
- **Load** — write the transformed data to a destination.

Example:

```text
Read orders.csv       → Extract
Calculate revenue     → Transform
Insert into PostgreSQL → Load
```

---

## 3. Extract

Data can be extracted from:

- CSV
- JSON
- Parquet
- APIs
- Databases

Example with Pandas:

```python
import pandas as pd

df = pd.read_parquet("yellow_tripdata_2026-01.parquet")
```

The output is a Pandas DataFrame that can be inspected and transformed.

---

## 4. Transform

Transformation changes data into a form suitable for analysis or storage.

Common transformations include:

- Renaming columns
- Converting data types
- Handling missing values
- Filtering rows
- Removing duplicates
- Creating calculated columns
- Validating records

Example from the NYC Taxi pipeline:

```python
df["trip_duration_minutes"] = (
    df["tpep_dropoff_datetime"] -
    df["tpep_pickup_datetime"]
).dt.total_seconds() / 60
```

This creates a new feature representing trip duration.

---

## 5. Load

Loading writes transformed data to a destination.

Possible destinations include:

- PostgreSQL
- Data warehouses
- Parquet files
- Object storage

Example:

```python
df.to_sql(
    "taxi_trips",
    engine,
    if_exists="append",
    index=False
)
```

---

## 6. Modular Pipeline Design

Instead of writing the entire pipeline in one Python file, responsibilities should be separated.

Week 3 structure:

```text
src/
├── main.py
└── pipeline/
    ├── __init__.py
    ├── api_extract.py
    ├── config.py
    ├── database.py
    ├── extract.py
    ├── load.py
    └── transform.py
```

Responsibilities:

```text
extract.py    → Retrieve data
transform.py  → Clean/transform data
load.py       → Write data to destination
database.py   → Database connection logic
config.py     → Configuration
main.py       → Coordinate pipeline execution
```

Advantages of modular design:

- Easier to understand
- Easier to test
- Easier to debug
- Easier to maintain
- Components can be reused

---

## 7. Functions

Functions make pipeline logic reusable.

Example:

```python
def calculate_revenue(quantity, unit_price):
    return quantity * unit_price
```

A function should ideally have one clear responsibility.

---

## 8. Type Hints

Type hints document expected input and output types.

Example:

```python
def calculate_revenue(
    quantity: int,
    unit_price: float
) -> float:
    return quantity * unit_price
```

Type hints improve:

- Readability
- Maintainability
- IDE assistance
- Error detection

---

## 9. API Extraction

Week 3 also included API extraction using Python requests.

General flow:

```text
API
 ↓
HTTP Request
 ↓
JSON Response
 ↓
Validation
 ↓
Pandas DataFrame
```

The API practice used JSONPlaceholder.

Important API concepts included:

- `requests.Session`
- HTTP requests
- JSON decoding
- HTTP status checking
- Timeouts
- Retries

---

## 10. HTTP Status Validation

`raise_for_status()` checks whether an HTTP request failed.

Example:

```python
response = session.get(url, timeout=10)
response.raise_for_status()
```

HTTP errors should not be silently ignored.

---

## 11. Timeout

A timeout prevents a request from waiting forever.

Example:

```python
response = session.get(url, timeout=10)
```

This is important because external services may become slow or unavailable.

---

## 12. Retry and Backoff

Temporary network/server failures should sometimes be retried.

The Week 3 API client used retry logic for errors such as:

```text
500
502
503
504
```

A retry means trying the operation again.

Backoff means waiting between retry attempts rather than repeatedly sending requests immediately.

Conceptually:

```text
Request fails
     ↓
Wait
     ↓
Retry
     ↓
Wait longer if necessary
     ↓
Retry again
```

Retries are useful for temporary failures, but permanent errors should eventually cause the pipeline to fail clearly.

---

## 13. Exception Handling

Exceptions allow pipeline failures to be handled intentionally.

Example:

```python
try:
    response = client.get()
except Exception as error:
    print(error)
```

Production pipelines should:

- Detect failures
- Record useful error information
- Retry when appropriate
- Stop safely when recovery is impossible

---

## 14. Logging

Logging records what happens during pipeline execution.

Useful log messages include:

```text
Pipeline started
Extraction completed
100 records extracted
Transformation completed
Loading started
Retry attempt
Pipeline completed
Pipeline failed
```

Logging is preferred over random `print()` statements for production-style pipelines because logs provide operational evidence and help diagnose failures.

---

## 15. Data Validation with Pydantic

Pydantic can validate incoming records against an expected schema.

Conceptual example:

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
```

If incoming data does not satisfy the expected schema, validation can fail instead of allowing incorrect data to silently enter the pipeline.

---

## 16. PostgreSQL and SQLAlchemy

Week 3 used SQLAlchemy to connect Python with PostgreSQL.

Architecture:

```text
Python
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

Example:

```python
from sqlalchemy import create_engine

engine = create_engine(database_url)
```

Database configuration should be separated from transformation logic.

---

## 17. Environment and Configuration

Configuration values should be separated from business logic.

Examples:

- Database URL
- API URL
- Timeouts
- File paths
- Environment-specific settings

Sensitive credentials should not be committed to GitHub.

---

## 18. Testing with pytest

Automated tests verify that pipeline components behave correctly.

Command:

```bash
pytest
```

Week 3 finished with:

```text
3 passed
```

Tests included:

- API client creation
- Mock HTTP status behavior
- Patching `APIClient.get`

---

## 19. Mocking

Tests should not always call a real external API.

Mocking simulates external behavior.

Advantages:

- Faster tests
- Repeatable results
- No dependency on internet availability
- Failure scenarios can be tested safely

Example concept:

```text
Real API
   X
Mock response
   ↓
Pipeline test
```

---

## 20. Idempotency

An idempotent or safely rerunnable pipeline should not corrupt data or create unwanted duplicates when executed again.

Possible techniques include:

- Unique constraints
- UPSERT
- MERGE
- `NOT EXISTS`
- Controlled replacement
- Watermarks/incremental loading

This becomes especially important when pipelines are scheduled automatically.

---

## 21. NYC Taxi Data Inspection

The January 2026 NYC Yellow Taxi dataset contained:

```text
3,724,889 rows
20 original columns
```

A `trip_duration_minutes` column was also created.

The dataset was inspected for:

- Missing values
- Duplicate rows
- Invalid/suspicious distances
- Negative fares
- Pickup/dropoff timestamp problems

Important findings included:

- No exact duplicate rows
- Some fields contained significant missing values
- Some trips had zero distance
- Some fares were negative
- One record had pickup time later than dropoff time
- Some pickup and dropoff timestamps were identical

The lesson was not to automatically delete unusual records without understanding their meaning.

---

## 22. Week 3 Pipeline Architecture

```text
NYC Taxi Data
      |
      v
   Extract
      |
      v
  Transform
      |
      v
    Load
      |
      v
 PostgreSQL
```

API practice:

```text
JSONPlaceholder API
        |
        v
     Session
        |
        v
 Retry / Backoff
        |
        v
 HTTP Validation
        |
        v
 Pydantic Validation
        |
        v
    DataFrame
```

---

## 23. Key Week 3 Lessons

- ETL means Extract, Transform, Load.
- Separate pipeline responsibilities into modules.
- Functions make logic reusable.
- Type hints improve code clarity.
- External APIs can fail and require defensive programming.
- Use timeouts for network requests.
- Retry temporary failures with backoff.
- Validate incoming data.
- Use structured logging to understand pipeline execution.
- Test important behaviors with pytest.
- Mock external dependencies during tests.
- Keep configuration separate from processing logic.
- Design pipelines so they can be safely rerun.
