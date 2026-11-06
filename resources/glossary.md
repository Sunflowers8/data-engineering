# Data Engineering Glossary

Concise definitions with practical examples.

## Fundamental Concepts

**Data Engineering:** Designing and maintaining systems that
collect, process, store and deliver reliable data.

**Data Pipeline:** A sequence of steps that moves and prepares
data from a source to a destination.

**ETL:** Extract, Transform, Load. Data is transformed before
being loaded into its destination.

**ELT:** Extract, Load, Transform. Data is loaded first and
transformed in the destination system.

**Batch Processing:** Processing data at scheduled intervals.

**Streaming:** Processing continuously arriving events.

**Data Warehouse:** A system designed for analytical queries
and reporting.

**Data Lake:** Storage for large amounts of data in various
formats, often including raw data.

**Parquet:** Column-oriented file format commonly used for
efficient analytical storage.

**Partitioning:** Dividing data into groups, commonly by date,
to reduce unnecessary scans.

**Clustering:** Organizing related data to improve selected
query patterns.

## SQL and Modeling

**Primary Key:** A column or combination that uniquely
identifies a row.

**Business Key:** Identifier supplied by the business system,
such as `order_id`.

**Surrogate Key:** Internally generated identifier used by
a data model.

**Grain:** What exactly one row in a table represents.

**Fact Table:** Contains measurable business events, such
as orders or payments.

**Dimension Table:** Describes business entities, such as
customers or products.

**Star Schema:** A dimensional model with a central fact
table connected to dimensions.

**SCD Type 1:** Updates dimension attributes without
preserving previous versions.

**SCD Type 2:** Preserves historical dimension versions.

**CTE:** Common Table Expression; a named intermediate SQL
query defined using `WITH`.

**Window Function:** Performs calculations across related
rows while preserving individual row detail.

## Reliability

**Idempotency:** Reprocessing the same input produces the
same intended business state without unwanted duplicates.

**Deduplication:** Selecting or retaining one canonical
record for a defined key.

**Watermark:** A checkpoint indicating how far ingestion
or processing has progressed.

**Incremental Loading:** Processing new or changed records
rather than rebuilding all historical data.

**Backfill:** Processing or reprocessing an older period.

**Late-Arriving Data:** Data received after its expected
processing window.

**Upsert:** Insert a new record or update an existing one.

**MERGE:** SQL operation that conditionally updates,
inserts or sometimes deletes records using matching keys.

**Data Quality Test:** A check enforcing a data expectation,
such as a unique order ID.

**Quarantine:** Separating invalid records and recording
the reasons for rejection.

**Rollback:** Reversing uncommitted database changes
after a failed transaction.

## Tools and Processing

**DuckDB:** Analytical SQL database suitable for local
data processing.

**dbt:** Tool for organizing, running, testing and documenting
SQL-based transformations.

**Airflow:** Workflow orchestrator for scheduling tasks,
managing dependencies and monitoring execution.

**DAG:** Directed Acyclic Graph; tasks and dependencies
without circular paths.

**PySpark:** Python interface for distributed processing
with Apache Spark.

**Shuffle:** Redistribution of data between Spark workers
during certain operations.

**Data Skew:** Uneven distribution of records or work.

**Kafka:** Distributed event-streaming platform.

**Docker:** Containerization platform for packaging
applications with their dependencies.

**CI/CD:** Practices for automating software validation
and delivery.

## ShopFlow Example

- Business key: `order_id`
- Fact grain: one row per business order
- Deduplication: newest `updated_at`, then `source_seq`
- Idempotency: conditional business-key upserts
- Data quality: unique keys and valid relationships
- Orchestration: ingestion → dbt transformation → tests
