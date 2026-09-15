# Data Engineering Learning Repository

This repository documents my hands-on Data Engineering learning and internship practice.

## Week 1: Data Engineering Foundations

### Concepts Learned

- Modern data stack
- Source, ingestion, storage, transformation, and serving
- Batch vs streaming processing
- Data warehouse, data lake, and lakehouse
- OLTP vs OLAP
- Row-oriented vs columnar storage
- ETL fundamentals

### Tools Setup

- Python
- VS Code
- Git
- GitHub
- PostgreSQL 16
- Pandas

Docker setup is pending due to compatibility considerations with my current macOS environment.

### Practical Work

During Week 1, I:

- Worked with CSV datasets using Python
- Read and transformed data using Pandas
- Handled missing values
- Created a basic ETL workflow
- Installed and configured PostgreSQL
- Created a PostgreSQL database and table
- Loaded cleaned CSV data into PostgreSQL
- Practiced SQL queries on the loaded data
- Used Git for version control
- Published the project to GitHub

## Current Pipeline

Raw CSV
→ Python/Pandas
→ Cleaned CSV
→ PostgreSQL
→ SQL Analytics

## Repository Structure

- `clean_data.py` - Data cleaning practice
- `pandas_pipeline.py` - Pandas pipeline practice
- `read_csv.py` - CSV reading practice
- `salary_pipeline.py` - Salary transformation pipeline
- `first.sql` - SQL practice
- `architecture/` - Data architecture documentation
- CSV files - Sample raw, transformed, and cleaned datasets

## Next Steps

Week 2 will focus on SQL for Data Engineering.