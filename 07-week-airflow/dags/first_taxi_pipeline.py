from datetime import timedelta
import pendulum
from airflow.sdk import dag, task


@dag(
    dag_id="first_taxi_pipeline",
    start_date=pendulum.datetime(2026, 10, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["learning", "nyc-taxi"],
)
def first_taxi_pipeline():

    @task
    def start_pipeline():
        print("🚕 Starting NYC Taxi pipeline!")


    @task(
        retries=2,
        retry_delay=timedelta(seconds=30),
    )
    def process_taxi_data():
        from pathlib import Path

        marker = Path("/tmp/airflow_week7_retry_demo")

        if not marker.exists():
            marker.write_text("first attempt completed")
            print("Simulating a temporary database connection failure!")
            raise ConnectionError("Temporary connection failure")

        print("Connection restored!")
        print("Processing NYC Taxi trip records...")
        print("Simulated processing complete!")

    @task
    def finish_pipeline():
        print("✅ NYC Taxi pipeline completed!")

    start = start_pipeline()
    process = process_taxi_data()
    finish = finish_pipeline()

    start >> process >> finish


first_taxi_pipeline()
