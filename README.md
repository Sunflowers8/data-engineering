
# Data Engineering Internship Journey 🚀

Welcome to my Data Engineering learning portfolio!

This repository documents my hands-on learning, technical exercises, SQL queries, Python pipelines, data modeling projects, and engineering experiments during a structured 10-week Data Engineering internship.

The learning roadmap follows the **Data Engineer Foundation Course**, with an emphasis on production-oriented engineering practices, reproducible pipelines, testing, documentation, and version control.

## 📊 Learning Roadmap

| Week | Topic | Status |
|------|-------|--------|
| 01 | Data Engineering Foundations & Environment Setup | ✅ Completed |
| 02 | Advanced SQL for Data Engineers | ✅ Completed |
| 03 | Python for Production & Data Pipelines | ✅ Completed |
| 04 | Data Modeling & Dimensional Modeling | ✅ Completed |
| 05 | Cloud Data Warehousing & Object Storage | 🔄 In Progress |
| 06 | dbt & Analytics Engineering | ⏳ Upcoming |
| 07 | Apache Airflow & Pipeline Orchestration | ⏳ Upcoming |
| 08 | Docker, CI/CD & Data Quality | ⏳ Upcoming |
| 09 | PySpark & Distributed Processing | ⏳ Upcoming |
| 10 | Kafka, Streaming & Capstone Project | ⏳ Upcoming |

## 🏆 Month 1 Milestone

**Weeks 1–4 completed.**

During the first month, I developed foundational skills in SQL, Python data pipelines, and dimensional modeling.

### Key Accomplishments

- Set up a local Data Engineering development environment.
- Practiced advanced PostgreSQL queries.
- Built a modular Python ETL pipeline using NYC Taxi data.
- Implemented API extraction with retries and error handling.
- Used Pandas for data cleaning and transformation.
- Practiced automated testing with pytest.
- Designed a dimensional star schema for NYC Taxi analytics.
- Created date, location, vendor, and payment-type dimensions.
- Practiced loading taxi trip data into a fact table.
- Documented technical exercises, project decisions, and lessons learned.
- Maintained a version-controlled GitHub portfolio.

📄 **[Read My Month 1 Internship Report](progress/month-1-report.md)**

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

Each module is organized to document:

- Learning objectives and concepts studied
- Technologies and tools used
- Practical exercises and implementation code
- Mini-projects and engineering decisions
- Challenges encountered and solutions
- Key takeaways and areas for improvement

## 🛠️ Technologies & Tools

### Used During Month 1

- **Programming:** Python, SQL
- **Database:** PostgreSQL
- **Python Libraries:** Pandas, Requests, Pydantic, pytest
- **Development:** VS Code, Git, GitHub
- **Database Tools:** DBeaver
- **Data Formats:** CSV, JSON, Parquet

### Upcoming Technologies

- Cloud warehouses: BigQuery or Snowflake
- Object storage: Amazon S3 or Google Cloud Storage
- dbt
- Apache Airflow
- Docker and Docker Compose
- GitHub Actions
- PySpark
- Apache Kafka

## 🚕 Featured Project: NYC Taxi Data Pipeline

An end-to-end learning project built using New York City taxi trip data.

### Pipeline Architecture

```text
NYC Taxi Dataset
       |
       v
Python Extraction
       |
       v
Pandas Transformation
       |
       v
PostgreSQL Loading
       |
       v
Dimensional Star Schema
       |
       v
SQL Analytics
```

### Project Components

- **Week 2:** Advanced SQL exercises and NYC Taxi queries
- **Week 3:** Modular Python ETL pipeline and API extraction
- **Week 4:** Star schema design, dimensions, fact table, and ERD
- **Week 5:** CSV vs Parquet comparison and partitioned storage experiments (in progress)

## 📈 Module 5 Progress

Currently studying Cloud Data Warehousing and Object Storage.

### Completed Experiment: CSV vs Parquet

Using the same 500,000 NYC Taxi records:

| Metric | CSV | Parquet |
|--------|-----|---------|
| File size | 59.40 MB | 11.11 MB |
| Selected-column read time | 0.5276 sec | 0.3489 sec |

**Observation:** Parquet reduced file size by approximately 81.31% and was faster in this single read experiment.

Further work will cover date-based partitioning, cloud object storage, external tables, native warehouse tables, and query cost optimization.

## 🎯 Learning Objectives

By the end of this internship, I aim to:

1. Write efficient, maintainable SQL for analytical workloads.
2. Build reliable, tested, and repeatable Python pipelines.
3. Design dimensional data models for business analytics.
4. Work with cloud data warehouses and object storage.
5. Develop dbt transformation projects.
6. Orchestrate pipelines using Apache Airflow.
7. Understand Docker, CI/CD, and data quality practices.
8. Gain practical exposure to PySpark and Kafka.
9. Deliver a documented end-to-end Data Engineering capstone.

## 📚 Progress Reports

| Report | Status |
|--------|--------|
| [Month 1 — Foundations, SQL, Python & Modeling](progress/month-1-report.md) | ✅ Published |
| Month 2 — Cloud Warehouse, dbt & Orchestration | ⏳ Upcoming |

---

*This repository is a learning portfolio. Projects and implementations are progressively improved as new engineering concepts are introduced.*
