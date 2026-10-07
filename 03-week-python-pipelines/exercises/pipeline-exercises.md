# Week 3 — Python Data Pipeline Exercises

These exercises document the practical concepts covered during Week 3.

---

## Exercise 1 — Identify ETL Stages

Given the following tasks:

1. Read `orders.csv`.
2. Calculate `revenue = quantity * unit_price`.
3. Insert the transformed records into PostgreSQL.

Identify the ETL stages.

### Answer

```text
Extract   = Read orders.csv
Transform = Calculate revenue
Load      = Insert into PostgreSQL
```

---

## Exercise 2 — CSV Processing

Given employee data in a CSV file:

1. Read the file using Python.
2. Convert salary values to numeric values.
3. Filter employees belonging to the Data department.
4. Find employees earning more than 40,000.
5. Calculate a 10% salary increase.
6. Save the transformed records into a new CSV.

Skills practiced:

- CSV reading
- Loops
- Conditions
- Numeric conversion
- Filtering
- Transformation
- Writing output files

---

## Exercise 3 — Pandas Data Inspection

Using a Pandas DataFrame:

1. Display the first rows.
2. Find the shape.
3. Display column names.
4. Select a single column.
5. Calculate the mean salary.

Useful operations:

```python
df.head()
df.shape
df.columns
df["salary"]
df["salary"].mean()
```

---

## Exercise 4 — Missing Values

Using a dataset containing missing values:

1. Identify missing values.
2. Count missing values per column.
3. Fill missing age using the mean age.
4. Fill missing department with `"Unknown"`.
5. Fill missing salary using the mean salary.

Useful operations:

```python
df.isnull()
df.isnull().sum()
df.fillna()
df.dropna()
```

---

## Exercise 5 — Grouping and Aggregation

Calculate:

- Employee count by department
- Average salary by department
- Maximum salary by department
- Minimum salary by department

Practice:

```python
df.groupby("department").size()

df.groupby("department")["salary"].agg([
    "mean",
    "max",
    "min"
])
```

Understand the difference between:

```python
.count()
```

and:

```python
.size()
```

---

## Exercise 6 — NYC Taxi Data Inspection

Inspect the NYC Yellow Taxi dataset.

Check:

- Number of rows and columns
- Column names
- Missing values
- Exact duplicates
- Zero or negative trip distance
- Negative fare amount
- Pickup timestamp greater than dropoff timestamp
- Pickup timestamp equal to dropoff timestamp

### Findings from the dataset

```text
Rows: 3,724,889
Original columns: 20
Exact duplicates: 0
```

A new field was created:

```text
trip_duration_minutes
```

The exercise demonstrated that suspicious values should be investigated instead of blindly deleted.

---

## Exercise 7 — Modular ETL Pipeline

Organize pipeline code into:

```text
pipeline/
├── extract.py
├── transform.py
├── load.py
├── database.py
└── config.py
```

Explain each responsibility.

### Answer

```text
extract.py
Retrieve data from the source.

transform.py
Clean, validate, and transform data.

load.py
Write transformed data to the destination.

database.py
Manage database connection logic.

config.py
Store/configure pipeline settings.
```

---

## Exercise 8 — API Client

Create an API client that:

1. Uses a `requests.Session`.
2. Sends a GET request.
3. Uses a timeout.
4. Calls `raise_for_status()`.
5. Returns decoded JSON.

Conceptual flow:

```text
API → Request → HTTP validation → JSON → Python
```

---

## Exercise 9 — Retry and Backoff

Configure the API client to retry temporary server failures.

Retry status codes used during practice included:

```text
500
502
503
504
```

Questions:

1. Why should a temporary 503 error sometimes be retried?
2. Why should retries have a limit?
3. What is backoff?
4. Why is retrying every error dangerous?

---

## Exercise 10 — Pydantic Validation

Create a model representing expected API data.

Example concept:

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
```

Test:

1. A valid record.
2. A record missing a required field.
3. A record containing an invalid value/type.

---

## Exercise 11 — Error Handling

Simulate an API failure.

The pipeline should:

1. Detect the failure.
2. Log useful information.
3. Retry when the failure is temporary.
4. Stop clearly when retries are exhausted.

---

## Exercise 12 — PostgreSQL Loading

Using SQLAlchemy:

1. Create a PostgreSQL engine.
2. Connect the transformed DataFrame to the database.
3. Load records into a destination table.
4. Verify the number of records using SQL.

Architecture:

```text
Pandas DataFrame
       |
       v
   SQLAlchemy
       |
       v
   PostgreSQL
```

---

## Exercise 13 — pytest

Create automated tests for the API extraction component.

Week 3 tests included:

- API client initialization
- Mock status behavior
- Patching `APIClient.get`

Run:

```bash
pytest
```

Expected completed Week 3 result:

```text
3 passed
```

---

## Exercise 14 — Mocking

Explain why a real API should not be required for every unit test.

### Answer

Mocking makes tests:

- Faster
- Predictable
- Repeatable
- Independent of external network availability

It also allows failure scenarios to be simulated safely.

---

## Exercise 15 — Idempotency

Question:

What could happen if a pipeline inserts the same records every time it runs?

### Answer

Duplicate records may be created.

Possible protections include:

- Unique constraints
- UPSERT
- MERGE
- `NOT EXISTS`
- Controlled replacement

---

# Exam-Style Questions

## Question 1

What are the three main ETL stages?

### Answer

```text
Extract
Transform
Load
```

---

## Question 2

Why should `extract.py`, `transform.py`, and `load.py` be separated?

### Answer

Separation makes the pipeline easier to understand, test, maintain, debug, and reuse.

---

## Question 3

What is a timeout?

### Answer

A timeout limits how long a program waits for an external request before treating it as a failure.

---

## Question 4

What is retry/backoff?

### Answer

Retry means attempting a failed operation again. Backoff introduces a delay between retries to avoid repeatedly overwhelming a failing service.

---

## Question 5

Why use logging?

### Answer

Logging provides evidence of pipeline execution and helps identify where and why failures occurred.

---

## Question 6

Why use Pydantic?

### Answer

Pydantic validates incoming data against an expected schema before the data continues through the pipeline.

---

## Question 7

Why mock an API during testing?

### Answer

Mocking removes dependency on the real external API and makes tests predictable and repeatable.

---

## Question 8

What makes a pipeline safely rerunnable?

### Answer

A safely rerunnable pipeline produces a correct result even when executed again and does not create unintended duplicates or corrupt existing data.

---

# Week 3 Practical Checklist

- [x] CSV processing
- [x] Pandas transformations
- [x] Missing-value handling
- [x] Grouping and aggregation
- [x] NYC Taxi data inspection
- [x] Modular Python pipeline
- [x] PostgreSQL integration
- [x] API extraction
- [x] Retry/backoff
- [x] Timeout handling
- [x] Pydantic validation
- [x] Error handling
- [x] Logging
- [x] pytest
- [x] Mocking
- [x] 3 tests passing
