
import pendulum
import subprocess

from airflow.sdk import dag, task


@dag(
    dag_id="nyc_taxi_data_check",
    start_date=pendulum.datetime(2026, 10, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["week7", "duckdb", "nyc-taxi"],
)
def nyc_taxi_data_check():

    @task
    def check_taxi_records():

        query_script = """
import duckdb

database = "/opt/airflow/data/airflow_taxi_practice.duckdb"

with duckdb.connect(database, read_only=True) as con:
    count = con.execute(
        "SELECT COUNT(*) FROM main.taxi_native"
    ).fetchone()[0]

    print(f"NYC Taxi records: {count:,}")

    if count != 500_000:
        raise ValueError(f"Unexpected record count: {count}")

print("Data quality check passed!")
"""

        subprocess.run(
            [
                "/opt/airflow/taxi-venv/bin/python",
                "-c",
                query_script,
            ],
            check=True,
        )

    check_taxi_records()


nyc_taxi_data_check()
