# Week 01 — Data Engineering Foundations Notes

## 1. What is Data Engineering?

Data Engineering focuses on collecting, moving, storing, cleaning and
preparing data so that it can be used for analytics, reporting,
applications and machine learning.

A Data Engineer builds and maintains the systems and pipelines that move
data from its source to a usable destination.

---

## 2. Modern Data Stack

The basic flow studied during Week 1 is:

Source → Ingestion → Storage → Transformation → Serving

### Source

The source is where the data originally comes from.

Examples:
- CSV files
- Websites
- Applications
- APIs
- Databases
- Sensors

### Ingestion

Ingestion means collecting or moving data from the source into a system
where it can be stored or processed.

### Storage

Storage is where the collected data is kept.

Examples:
- PostgreSQL
- Data Warehouse
- Data Lake

### Transformation

Transformation means cleaning, changing and preparing data for use.

Examples:
- Filling missing values
- Removing duplicates
- Changing data types
- Calculating new values
- Aggregating data

In my Week 1 practical work, Pandas performed transformation.

### Serving

Serving means making processed data available to downstream users or systems.

Examples:
- BI dashboards
- Reports
- Analytics
- Applications
- Machine Learning systems

---

## 3. Batch vs Streaming

### Batch Processing

Batch processing processes data in groups, usually according to a schedule.

Examples:
- Monthly payroll
- Nightly reports
- Daily sales processing

### Streaming Processing

Streaming processes continuously arriving data in near real time.

Examples:
- Fraud detection
- GPS tracking
- Live application events

Streaming is not always necessary because it can be more complex and
expensive than batch processing.

---

## 4. Data Warehouse

A Data Warehouse stores structured, cleaned and analytics-ready data.

It is commonly used for:
- Reporting
- Business Intelligence
- Analytics
- Aggregations

---

## 5. Data Lake

A Data Lake can store large amounts of raw data.

It can contain:
- Structured data
- Semi-structured data
- Unstructured data

The data does not necessarily need to be cleaned before being stored.

---

## 6. Lakehouse

A Lakehouse combines characteristics of a Data Lake and Data Warehouse.

It provides flexible storage while also supporting structured data
management and analytics.

---

## 7. OLTP vs OLAP

### OLTP — Online Transaction Processing

Used for running day-to-day operations.

Examples:
- Creating an order
- Updating a customer
- Recording a payment

Typical characteristics:
- Many short transactions
- INSERT / UPDATE / DELETE
- Operational applications

### OLAP — Online Analytical Processing

Used for analyzing data.

Examples:
- Average monthly sales
- Revenue analysis
- Customer trends

Typical characteristics:
- Large analytical queries
- Historical data
- Aggregations

Memory:

OLTP = Run the business

OLAP = Analyze the business

---

## 8. Row-Oriented vs Columnar Storage

### Row-Oriented

Stores the values belonging to a record together.

Useful for:
- OLTP
- Frequent inserts and updates
- Retrieving complete records

### Columnar

Stores values belonging to the same column together.

Useful for:
- OLAP
- Aggregations
- Analytical queries
- Queries that need only selected columns

Columnar storage can also provide efficient compression.

---

## 9. ETL

ETL means:

Extract → Transform → Load

### Extract

Read data from the source.

Week 1 example:
Reading `employees.csv`.

### Transform

Clean or modify the data.

Week 1 examples:
- Filling missing values
- Filtering data
- Calculating salary values
- Aggregating data

### Load

Write the processed data to its destination.

Week 1 examples:
- Writing a cleaned CSV
- Loading employee data into PostgreSQL

---

## 10. Pandas

Important Pandas operations practiced:

Read CSV:

    pd.read_csv()

Preview data:

    df.head()

Dataset dimensions:

    df.shape

Columns:

    df.columns

Detect missing values:

    df.isnull().sum()

Fill missing values:

    df["column"].fillna(value)

Filter:

    df[(condition1) & (condition2)]

Group data:

    df.groupby()

Aggregate:

    .mean()
    .min()
    .max()
    .count()
    .agg()

Save CSV:

    df.to_csv("file.csv", index=False)

Important:

`&` is used between Pandas conditions, and each condition should normally
be placed inside parentheses.

---

## 11. PostgreSQL

Week 1 database:

    employee_db

Table:

    employee

SQL operations practiced:

- SELECT
- FROM
- WHERE
- AND
- OR
- ORDER BY
- LIMIT
- AVG
- GROUP BY

Example:

    SELECT name,
           department,
           salary
    FROM employee
    WHERE salary > 30000
    ORDER BY salary DESC;

---

## 12. Git and GitHub

Git is the version-control system used locally.

GitHub hosts the Git repository remotely.

Important workflow:

    git status
        ↓
    git add .
        ↓
    git commit -m "message"
        ↓
    git push

### git status

Shows the current state of the repository.

### git add .

Stages changes for the next commit.

### git commit

Creates a local snapshot of the staged changes.

### git push

Sends committed changes to the remote GitHub repository.

Memory:

ADD → COMMIT → PUSH

---

## 13. Docker

Docker runs applications inside containers.

Week 1 local setup:

Docker CLI → Colima → QEMU → Linux VM → Docker Engine → Container

The installation was verified using:

    docker run hello-world

and successfully returned:

    Hello from Docker!

Useful command after restarting the Mac:

    colima start

Check runtime:

    colima status

---

## 14. DBeaver

DBeaver provides a graphical interface for working with databases.

During Week 1 it was connected to:

- PostgreSQL 16
- Database: employee_db
- Table: employee

I used the SQL Editor to execute PostgreSQL queries and inspect their results.

---

# Week 1 Practical Pipeline

Raw CSV
   ↓
Python / Pandas
   ↓
Cleaning & Transformation
   ↓
Processed CSV
   ↓
PostgreSQL
   ↓
SQL Queries
   ↓
DBeaver / Analytics

---

# Week 1 Key Takeaways

1. Data Engineering is about moving and preparing reliable data.
2. A basic data stack consists of Source → Ingestion → Storage →
   Transformation → Serving.
3. Batch processes groups of data while streaming processes continuously
   arriving data.
4. Warehouses, lakes and lakehouses serve different storage requirements.
5. OLTP runs operational transactions while OLAP supports analytics.
6. Pandas can clean and transform datasets.
7. PostgreSQL stores structured relational data that can be queried using SQL.
8. ETL means Extract → Transform → Load.
9. Git tracks changes and GitHub stores the remote repository.
10. Docker containers provide reproducible application environments.