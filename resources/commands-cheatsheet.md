# Data Engineering — Commands Cheatsheet

Quick reference for my data engineering practice on macOS.

## 1. Terminal and Files

| Command | Purpose |
|---|---|
| `pwd` | Show current directory |
| `ls -la` | List files, including hidden files |
| `cd folder_name` | Enter a directory |
| `cd ..` | Move to parent directory |
| `mkdir -p folder` | Create a directory |
| `touch file.py` | Create an empty file |
| `cat file.txt` | Display file contents |
| `find . -name "*.sql"` | Find SQL files |

## 2. Python Environment

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install duckdb pandas pytest
python script.py
python -m pytest -v
deactivate
```

## 3. Git and GitHub

```bash
git status
git branch
git add path/to/file
git diff --cached
git commit -m "Describe changes"
git push origin main
git pull origin main
git log --oneline -5
```

Always check staged files before committing.

## 4. DuckDB

```bash
python -c "import duckdb; print(duckdb.__version__)"
```

Example Python connection:

```python
import duckdb

con = duckdb.connect("shopflow.duckdb")
result = con.execute("SELECT COUNT(*) FROM orders").fetchone()
print(result)
con.close()
```

## 5. dbt

```bash
dbt --version
dbt debug --profiles-dir .
dbt ls --profiles-dir .
dbt run --profiles-dir .
dbt test --profiles-dir .
dbt build --profiles-dir .
dbt run --select staging --profiles-dir .
dbt run --select fct_orders --profiles-dir .
dbt run --full-refresh --select fct_orders --profiles-dir .
```

Use full refresh carefully: it rebuilds an incremental model.

## 6. Airflow

Typical Airflow commands, when Airflow is installed:

```bash
airflow dags list
airflow tasks list shopflow_daily_pipeline
airflow dags list-import-errors
```

In a DAG:

```python
ingest >> transform >> test
```

The default `all_success` trigger rule blocks downstream
tasks if an upstream task ultimately fails.

## 7. Docker

```bash
docker --version
docker ps
docker ps -a
docker images
docker compose up -d
docker compose logs
docker compose down
```

## 8. ShopFlow Practice

```bash
python src/ingest.py --batch-date 2026-10-01
python src/ingest.py --batch-date 2026-10-02
python src/ingest.py --batch-date 2026-10-02
python src/ingest.py --batch-date 2026-10-01 --backfill
dbt build --profiles-dir .
```

**Reminder:** A successful command is not sufficient evidence
of data correctness. Verify row counts, keys and business totals.
