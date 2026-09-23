# Week 01 — Data Engineering Foundations

## Overview

Week 1 focused on building the fundamental skills and development environment required for the Data Engineering internship.

The main goal was to understand the basic flow of data through a pipeline while gaining hands-on experience with Python, Pandas, CSV files, PostgreSQL, SQL, Git, GitHub, Docker, and development tools.

By the end of the week, I built and practiced a simple ETL workflow:

```text
CSV File
   ↓
Python / Pandas
   ↓
Clean & Transform Data
   ↓
Processed CSV
   ↓
PostgreSQL
   ↓
SQL Analysis
```

---

## Topics Covered

- Python fundamentals
- Lists and dictionaries
- Functions and loops
- Conditional statements
- Reading and writing CSV files
- Pandas DataFrames
- Data cleaning
- Missing-value handling
- Filtering and aggregation
- Basic ETL concepts
- PostgreSQL fundamentals
- Basic SQL queries
- Git and GitHub workflow
- Docker fundamentals
- Development environment setup

---

## Tools Used

| Tool | Purpose |
|---|---|
| Python | Data processing and scripting |
| Pandas | Data cleaning and transformation |
| PostgreSQL | Relational database |
| DBeaver | SQL development and database management |
| Git | Version control |
| GitHub | Repository hosting |
| VS Code | Code editor |
| Docker | Containerization |
| Colima | Docker runtime on macOS |
| QEMU | Virtualization used by Colima |

---

# 1. Python Fundamentals

Practiced core Python concepts required for data engineering.

Topics included:

- Variables
- Lists
- Dictionaries
- Loops
- Conditional statements
- Functions
- Counters
- Filtering
- Aggregations
- Minimum and maximum calculations

Example:

```python
records = [120, 150, 90, 200, 140]

total = sum(records)
average = total / len(records)

print(total)
print(average)
```

Created functions for reusable logic:

```python
def classify_record(record):
    if record < 100:
        return "Low"
    elif record <= 180:
        return "Normal"
    else:
        return "High"
```

---

# 2. Working with CSV Files

Created employee datasets and learned how to read and process CSV files using Python.

Example dataset:

```text
name,age,department,salary
Simran,23,Data,35000
Ram,28,Finance,25000
Sita,26,Data,45000
Hari,31,HR,30000
Gita,25,Data,50000
```

Practiced:

- Reading CSV files
- Iterating through records
- Converting string values to numeric types
- Filtering records
- Transforming values
- Writing processed data to new CSV files

---

# 3. First ETL Pipeline

Built a simple ETL pipeline using Python.

### Extract

Read employee information from:

```text
employees.csv
```

### Transform

Applied a 10% salary increase.

### Load

Saved the transformed data into:

```text
employees_updated.csv
```

This demonstrated the basic ETL process:

```text
Extract → Transform → Load
```

---

# 4. Pandas Fundamentals

Used Pandas for more efficient data manipulation.

Practiced:

```python
import pandas as pd

df = pd.read_csv("employees.csv")
```

Explored:

- `head()`
- `shape`
- `columns`
- Column selection
- Boolean filtering
- `mean()`
- `max()`
- `min()`
- `count()`
- `groupby()`
- `agg()`

Example:

```python
data_employees = df[
    (df["department"] == "Data") &
    (df["salary"] > 40000)
]
```

---

# 5. Data Cleaning

Created a dataset containing missing values and practiced detecting and cleaning them.

Used:

```python
df.isnull()
df.isnull().sum()
df.dropna()
df.fillna()
```

Missing values were handled using appropriate replacement strategies.

Examples included:

- Filling missing age using the mean age
- Replacing missing department with `Unknown`
- Filling missing salary using the mean salary

This produced a cleaned dataset:

```text
employees_cleaned.csv
```

---

# 6. Data Aggregation

Practiced summarizing employee data using Pandas.

Examples included:

```python
df.groupby("department")["salary"].mean()
```

and:

```python
df.groupby("department")["salary"].agg([
    "mean",
    "max",
    "min"
])
```

This introduced aggregation concepts frequently used in analytics and data engineering.

---

# 7. PostgreSQL

Installed and configured PostgreSQL locally.

Created a database:

```text
employee_db
```

Created an employee table containing:

```text
name
age
department
salary
```

Imported CSV data into PostgreSQL using:

```sql
\copy
```

This demonstrated the process:

```text
CSV
 ↓
PostgreSQL Table
 ↓
SQL Queries
```

---

# 8. SQL Fundamentals

Practiced foundational SQL operations.

Topics included:

- `SELECT`
- `FROM`
- `WHERE`
- `AND`
- `OR`
- `ORDER BY`
- `LIMIT`
- `AVG`
- `COUNT`
- `MAX`
- `GROUP BY`
- `HAVING`
- Column aliases

Example:

```sql
SELECT name,
       department,
       salary
FROM employee
WHERE salary > 30000
ORDER BY salary DESC;
```

Also practiced SQL clause order:

```text
SELECT
FROM
WHERE
GROUP BY
HAVING
ORDER BY
LIMIT
```

---

# 9. Git and GitHub

Learned the basic Git workflow used for version control.

```text
Working Directory
      ↓
git add
      ↓
Staging Area
      ↓
git commit
      ↓
Local Repository
      ↓
git push
      ↓
GitHub
```

Core commands practiced:

```bash
git status
git add .
git commit -m "message"
git push
```

A simple memory rule:

```text
ADD → COMMIT → PUSH
```

---

# 10. Docker Environment

Configured Docker on macOS using:

```text
Docker CLI
    ↓
Colima
    ↓
QEMU Virtual Machine
    ↓
Linux
    ↓
Docker Engine
    ↓
Containers
```

Verified the environment successfully using:

```bash
docker run hello-world
```

The successful `Hello from Docker!` output confirmed that the Docker environment was working correctly.

---

# Project Structure

```text
01-week-foundations/
│
├── README.md
│
├── notes/
│   └── foundations-notes.md
│
├── architecture/
│   └── week1_architecture.md
│
├── data/
│   ├── raw/
│   │   ├── employees.csv
│   │   └── employees_dirty.csv
│   │
│   └── processed/
│       ├── employees_cleaned.csv
│       ├── employees_pandas_updated.csv
│       └── employees_updated.csv
│
├── python/
│   ├── basics/
│   │   └── read_csv.py
│   │
│   ├── pandas/
│   │   ├── clean_data.py
│   │   └── pandas_pipeline.py
│   │
│   └── etl/
│       └── salary_pipeline.py
│
└── sql/
    └── first.sql
```

---

# Key Takeaways

By completing Week 1, I gained hands-on experience with the basic components of a data engineering workflow.

I learned how to:

- Work with Python data structures
- Read and write CSV files
- Clean and transform datasets with Pandas
- Build a basic ETL pipeline
- Load data into PostgreSQL
- Query data using SQL
- Organize a data engineering project
- Track code using Git and GitHub
- Run Docker containers locally

These foundations will support the more advanced topics covered in the following weeks, including advanced SQL, Python pipelines, data modeling, data warehouses, dbt, Airflow, Docker/CI/CD, PySpark, and Kafka.

---

## Status

**Week 01 — Completed ✅**