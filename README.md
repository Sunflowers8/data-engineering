
# Data Engineering Internship Journey 🚀

Welcome to my Data Engineering learning portfolio!

This repository documents my hands-on learning, technical exercises, SQL queries, Python pipelines, dimensional modeling, and engineering projects during a structured 10-week Data Engineering internship.

The roadmap follows the **Data Engineer Foundation Course**, focusing on reliable data pipelines, production-oriented Python, SQL, cloud warehousing, testing, documentation, and version control.

## 📊 Learning Roadmap

| Week | Topic | Status |
|------|-------|--------|
| 01 | Data Engineering Foundations & Environment Setup | ✅ Completed |
| 02 | Advanced SQL for Data Engineers | ✅ Completed |
| 03 | Python for Production & Data Pipelines | ✅ Completed |
| 04 | Data Modeling & Dimensional Modeling | ✅ Completed |
| 05 | Cloud Data Warehousing & Object Storage | ✅ Local Coursework Completed |
| 06 | dbt & Analytics Engineering | ✅ Completed |
| 07 | Apache Airflow & Pipeline Orchestration | ✅ Completed |
| 08 | Docker, CI/CD & Data Quality | ✅ Completed |
| 09 | PySpark & Distributed Processing | ⏳ Upcoming |
| 10 | Kafka, Streaming & Capstone Project | ⏳ Upcoming |

**Note:** Week 5 local coursework, DataCamp training, and practical assessment are complete. Actual S3/GCS-to-Snowflake or BigQuery integration remains a future extension.

## 🏆 Month 1 Milestone — Weeks 1–4

During the first month, I developed foundational skills in Data Engineering, advanced SQL, Python pipelines, and dimensional modeling.

### Key Accomplishments

- Configured a local Data Engineering development environment.
- Practiced advanced PostgreSQL queries.
- Built a modular Python ETL pipeline using NYC Taxi data.
- Implemented API extraction with retries and error handling.
- Used Pandas for extraction, cleaning, and transformation.
- Practiced automated testing using pytest.
- Designed a star schema for NYC Taxi analytics.
- Created date, location, vendor, and payment-type dimensions.
- Loaded taxi trip data into a dimensional fact table.
- Documented technical decisions, exercises, and learning outcomes.
- Maintained a version-controlled GitHub portfolio.

📄 **[Month 1 Internship Report](progress/month-1-report.md)**

## ☁️ Month 2 Progress — Week 5

### Cloud Warehousing and Object Storage

Completed local practical exercises covering:

- Columnar storage and Parquet compression.
- Date-based Parquet partitioning.
- Object storage concepts using MinIO.
- Python Boto3 integration with S3-compatible storage.
- External file querying using DuckDB.
- Native versus external storage comparisons.
- Query benchmarking and execution-plan analysis.
- Storage lifecycle policies.
- Warehouse cost optimization.
- Snowflake architecture and security fundamentals.

### DataCamp Courses Completed

| Course | Duration | Status |
|---|---|---|
| Data Warehousing Concepts | 4 hours | ✅ Completed |
| Introduction to Snowflake | 2 hours | ✅ Completed |

**Total:** 6 hours of completed DataCamp coursework.

### Practical Results

| Metric | Result |
|---|---:|
| NYC Taxi records processed | 500,000 |
| Original CSV size | 59.40 MB |
| Converted Parquet size | 11.11 MB |
| Storage reduction | 81.31% |
| Date partitions | 8 |
| Parquet objects uploaded to MinIO | 8 |
| January 1 trip count | 66,984 |
| January 1 revenue | $1,973,735.87 |
| Final practice viva | 17/20 (85%) |

### Query Performance Benchmark

| Storage Approach | Median Query Time |
|---|---:|
| External Parquet (DuckDB) | 0.00534 seconds |
| Native DuckDB table | 0.00187 seconds |

The native DuckDB table was approximately 2.86 times faster in this small, warm-cache benchmark. Results are workload-dependent.

### Week 5 Data Pipeline Architecture

```text
NYC Taxi Dataset
       |
       v
Python / Pandas
       |
       v
Partitioned Parquet
       |
       v
Boto3 Upload
       |
       v
MinIO Object Storage
       |
       v
DuckDB + httpfs
       |
       v
SQL Queries & Validation
```

**Limitation:** MinIO provides a local S3-compatible environment, not an AWS deployment. Cloud warehouse loading into Snowflake or BigQuery has not been implemented.

## 📁 Repository Structure

```text
data-engineering/
│
├── 01-week-foundations/
├── 02-week-sql/
├── 03-week-python-pipelines/
├── 04-week-data-modeling/
├── 05-week-warehouse-storage/
├── 06-week-dbt/
├── 07-week-airflow/
├── 08-week-docker-cicd/
├── 09-week-pyspark/
├── 10-week-kafka-capstone/
├── data/
├── resources/
├── progress/
└── README.md
```

Each weekly module documents:

- Learning objectives and concepts studied
- Technologies and tools used
- Hands-on exercises and implementation code
- Mini-projects and engineering decisions
- Challenges encountered and solutions
- Testing and validation results
- Key takeaways and areas for improvement

## 🛠️ Technologies & Tools

### Technologies Practiced

| Category | Technologies |
|---|---|
| Programming | Python, SQL |
| Relational Database | PostgreSQL |
| Analytical Database | DuckDB |
| Python Libraries | Pandas, PyArrow, Requests, Boto3, Pydantic, pytest |
| Container Runtime | Docker, Colima |
| Object Storage | MinIO (S3-compatible) |
| Data Formats | CSV, JSON, Parquet |
| Development | VS Code, Git, GitHub |
| Database Management | DBeaver |
| Cloud Warehouse Learning | Snowflake through DataCamp |

### Upcoming Technologies

- dbt
- Apache Airflow
- Docker Compose and GitHub Actions
- PySpark
- Apache Kafka
- Cloud warehouse integration using Snowflake or BigQuery

## 🚕 Featured Project: NYC Taxi Data Engineering Pipeline

A progressive Data Engineering project built using New York City taxi trip records.

### Project Components

| Week | Implementation |
|---|---|
| Week 2 | Advanced SQL exercises and NYC Taxi analysis |
| Week 3 | Modular Python ETL and API extraction |
| Week 4 | Dimensional star schema and fact/dimension tables |
| Week 5 | Parquet partitioning, MinIO ingestion, DuckDB querying, and optimization |
| Week 6 | dbt transformation models and automated testing — in progress |

### Engineering Principles

- Modular pipeline development
- Data validation and error handling
- Reproducible transformations
- Separation of source data and analytical models
- Secure credential handling
- SQL query optimization
- Git-based documentation and version control

## 🎯 Learning Objectives

By the end of the internship, I aim to:

1. Write efficient SQL for analytical and engineering workloads.
2. Build reliable, tested, and repeatable Python pipelines.
3. Design dimensional data models for analytics.
4. Work with cloud warehouses and object storage.
5. Develop dbt staging, intermediate, and mart models.
6. Orchestrate pipelines using Apache Airflow.
7. Apply Docker, CI/CD, and data-quality practices.
8. Gain practical exposure to PySpark and Kafka.
9. Deliver a documented end-to-end Data Engineering capstone.

## 📚 Progress Reports

| Report | Status |
|---|---|
| [Month 1 — Foundations, SQL, Python & Modeling](progress/month-1-report.md) | ✅ Published |
| Month 2 — Warehousing, dbt & Orchestration | 🔄 In Progress |

---

*This repository documents a progressive Data Engineering learning journey. Projects are continuously improved as new concepts and production practices are introduced.*
