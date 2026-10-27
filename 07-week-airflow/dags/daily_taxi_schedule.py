
import pendulum
from airflow.sdk import dag, task


@dag(
    dag_id="daily_taxi_schedule",
    start_date=pendulum.datetime(
        2026, 10, 1, tz="Asia/Kathmandu"
    ),
    schedule="0 6 * * *",
    catchup=False,
    tags=["learning", "scheduling", "nyc-taxi"],
)
def daily_taxi_schedule():

    @task
    def generate_daily_report():
        print("🚕 Starting scheduled taxi report!")
        print("Generating daily report...")
        print("✅ Daily report task completed!")

    generate_daily_report()


daily_taxi_schedule()
