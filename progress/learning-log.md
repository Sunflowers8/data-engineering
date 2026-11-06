
# Data Engineering Internship — Learning Log

**Intern:** Simran Thapa  
**Organization:** Codavatar  
**Track:** Data Engineering  
**Period:** Weeks 1–8, with additional practical learning

## Month 1 — Foundations

### Week 1 — Python and Development Setup

**Activities**
- Practiced Python fundamentals and CSV processing.
- Set up VS Code, PostgreSQL, DBeaver and Git.
- Practiced basic SQL queries and aggregations.

**Key Learning**
Developed a foundation in Python programming, database access and version control.

### Week 2 — SQL for Analytics

**Activities**
- Practiced joins, CTEs and window functions.
- Worked with deduplication, ranking and running totals.
- Explored UPSERT, indexing and query execution plans.
- Queried a 500,000-row NYC Taxi sample.

**Key Learning**
Learned how SQL supports data preparation and analytical processing.

### Week 3 — Python Data Pipelines

**Activities**
- Built modular extraction, transformation and loading scripts.
- Used Pandas, SQLAlchemy and API requests.
- Practiced logging, retries, validation and exception handling.
- Added pytest unit tests and mocking exercises.

**Key Learning**
Understood the importance of modular code, error handling and automated validation.

### Week 4 — Dimensional Modeling

**Activities**
- Designed an NYC Taxi star schema.
- Created fact and dimension tables.
- Practiced surrogate keys, foreign keys and grain definitions.
- Investigated unmatched dimension records.
- Documented the schema using Mermaid.

**Key Learning**
Learned that clear table grain and dimension coverage are essential for reliable analytical results.

---

## Month 2 — Pipeline Engineering

### Week 5 — Storage and Warehousing

**Activities**
- Compared CSV and Parquet file formats.
- Practiced partitioned storage.
- Used DuckDB for analytical queries.
- Explored MinIO and cloud object storage concepts.
- Studied partition pruning and warehouse performance.

**Key Learning**
Understood how data format, layout and storage design affect analytical efficiency.

### Week 6 — dbt Transformations

**Activities**
- Configured dbt Core with DuckDB.
- Created staging and analytical models.
- Practiced `source()`, `ref()` and model dependencies.
- Explored incremental materialization.
- Ran data-quality tests.

**Results**
- Three models completed.
- Eleven tests passed during practice.

**Key Learning**
Learned to separate raw data standardization from business transformations and validate model outputs.

### Week 7 — Apache Airflow

**Activities**
- Practiced DAG development and task dependencies.
- Explored scheduling, retries and failure behavior.
- Integrated DuckDB and dbt processing.
- Reviewed execution logs and task status.
- Practiced workflow execution using a local environment.

**Results**
- Four successful pipeline tasks.
- Eleven dbt tests passed.

**Key Learning**
Understood how orchestration coordinates dependent tasks and helps diagnose failures.

### Week 8 — Docker and CI/CD

**Activities**
- Built a Python taxi revenue application.
- Created a Dockerfile and Docker Compose setup.
- Practiced building and running containers.
- Added automated unit tests.
- Configured GitHub Actions.

**Key Learning**
Understood how containerization and continuous integration support reproducible software development.

---

## Additional Practical Learning

### PySpark

- Processed NYC Taxi data using PySpark.
- Practiced filtering, aggregations and Parquet output.
- Explored partitions, shuffles and distributed processing.
- Learned when Spark is justified by data volume.

### Kafka

- Practiced producing and consuming JSON events.
- Worked with topics, partitions and offsets.
- Studied consumer behavior and replay safety.
- Explored the difference between batch and streaming workloads.

### ShopFlow Batch Pipeline

**Activities**
- Validated customer, order and payment data.
- Quarantined invalid records.
- Deduplicated records using timestamps and source sequence.
- Implemented incremental ingestion and conditional upserts.
- Designed an order-level fact table and customer dimension.
- Created dbt staging and mart models.
- Defined Airflow task dependencies and retries.
- Verified idempotent reruns and payment reconciliation.

**Verified Results**
- 12 customers.
- 24 unique orders.
- Nine passing dbt tests.
- No additional business records after repeated ingestion.
- Practical assessment: 96/100, including 20 grace marks.

**Areas for Improvement**
- Handling late-arriving updates.
- Supporting controlled historical backfills.
- Removing machine-specific paths from Airflow DAGs.
- Improving automated testing and reproducibility.

---

## Overall Learning Reflection

Across the first two months, I progressed from writing individual Python and SQL exercises to building connected data processing workflows.

The most valuable lesson has been that successful execution does not always mean the data is correct. Reliable engineering requires clear business rules, validation, safe reruns, failure handling and testing.

## Next Steps

1. Strengthen SQL and Python problem-solving.
2. Improve historical backfill and incremental logic.
3. Add more automated tests.
4. Practice cloud warehouse integrations.
5. Build a complete portfolio pipeline that another engineer can reproduce.

---

**Prepared by:** Simran Thapa
