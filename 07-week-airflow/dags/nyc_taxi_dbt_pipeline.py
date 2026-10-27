from datetime import timedelta
import subprocess
import pendulum

from airflow.sdk import dag, task


PYTHON = "/opt/airflow/taxi-venv/bin/python"
DBT = "/opt/airflow/taxi-venv/bin/dbt"
DATABASE = "/opt/airflow/data/airflow_taxi_practice.duckdb"
PROJECT = "/opt/airflow/nyc_taxi_dbt"
PROFILES = "/opt/airflow/taxi-dbt-profiles"


@dag(
    dag_id="nyc_taxi_dbt_pipeline",
    start_date=pendulum.datetime(2026, 10, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    tags=["week7", "dbt", "duckdb"],
)
def nyc_taxi_dbt_pipeline():

    @task
    def check_source_data():
        script = f"""
import duckdb

with duckdb.connect({DATABASE!r}, read_only=True) as con:
    count = con.execute(
        "SELECT COUNT(*) FROM main.taxi_native"
    ).fetchone()[0]

print(f"Source records: {{count:,}}")

if count != 500_000:
    raise ValueError(f"Expected 500,000 records, got {{count}}")
"""
        subprocess.run([PYTHON, "-c", script], check=True)

    @task(execution_timeout=timedelta(minutes=3))
    def run_dbt_models():
        subprocess.run(
            [
                DBT, "run",
                "--project-dir", PROJECT,
                "--profiles-dir", PROFILES,
            ],
            check=True,
        )

    @task(execution_timeout=timedelta(minutes=3))
    def run_dbt_tests():
        subprocess.run(
            [
                DBT, "test",
                "--project-dir", PROJECT,
                "--profiles-dir", PROFILES,
            ],
            check=True,
        )

    @task
    def confirm_pipeline_success():
        print("NYC Taxi pipeline completed successfully!")
        print("All dbt models and data tests passed.")

    check = check_source_data()
    models = run_dbt_models()
    tests = run_dbt_tests()
    success = confirm_pipeline_success()

    check >> models >> tests >> success


nyc_taxi_dbt_pipeline()
