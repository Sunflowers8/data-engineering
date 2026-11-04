
"""
ShopFlow daily batch pipeline.

Runs ingestion, dbt transformations, and data-quality
tests in the required order.
"""

from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator


# Project location on this workstation
PROJECT_DIR = Path(
    "/Users/Simran/Downloads/"
    "ShopFlow_Data_Engineering_Exam_Dataset"
)

PYTHON = "/Users/Simran/data-engineering/.venv/bin/python"
DBT = "/Users/Simran/data-engineering/.venv/bin/dbt"


with DAG(
    dag_id="shopflow_daily_pipeline",
    description="ShopFlow daily batch ingestion and dbt",
    start_date=datetime(2026, 10, 1),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    default_args={
        "owner": "data_engineering",
        "retries": 0,
    },
    tags=["shopflow", "batch"],
) as dag:

   
    ingest = BashOperator(
        task_id="ingest_clean",
        bash_command=(
            f"{PYTHON} src/ingest.py "
            "--batch-date {{{{ ds }}}}"
    ),
    cwd=str(PROJECT_DIR),
    retries=2,
    retry_delay=timedelta(minutes=5),
)


    transform = BashOperator(
        task_id="dbt_transform",
        bash_command=(
            f"{DBT} run --profiles-dir ."
        ),
        cwd=str(PROJECT_DIR),
    )

    test = BashOperator(
        task_id="dbt_tests",
        bash_command=(
            f"{DBT} test --profiles-dir ."
        ),
        cwd=str(PROJECT_DIR),
    )

    # Ingestion must finish before transformations begin.
    # Failed upstream tasks block downstream tasks.
    ingest >> transform >> test
    # Failure handling:
    # The ingestion task allows two retries with a five-minute delay.
    # If ingestion still fails, Airflow marks the task as failed.
    # The default all_success trigger rule prevents dbt transformations
    # and tests from running on incomplete upstream data.
    #
    # Safe backfill:
    # Historical batches can be reprocessed using an explicit date
    # and the --backfill option. Conditional upserts ensure that
    # rerunning an older batch does not duplicate business records.
    # 
    # Historical backfill:
    # Trigger the DAG for a selected historical date,
    # passing that date to the ingestion script.
    # Use the script's --backfill option when necessary.
    # Primary-key upserts prevent duplicate business records.
    
