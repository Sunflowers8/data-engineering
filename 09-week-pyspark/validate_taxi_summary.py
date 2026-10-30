from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum

output_path = (
    Path(__file__).resolve().parent
    / "data/daily_taxi_summary"
)

spark = (
    SparkSession.builder
    .appName("Week9TaxiValidation")
    .master("local[2]")
    .config("spark.driver.memory", "1g")
    .config("spark.sql.shuffle.partitions", "2")
    .getOrCreate()
)

try:
    spark.sparkContext.setLogLevel("ERROR")

    df = spark.read.parquet(str(output_path))

    total_trips = df.agg(
        spark_sum("total_trips")
    ).first()[0]

    summary_dates = df.count()

    invalid_rows = df.filter(
        col("pickup_date").isNull()
        | (col("total_trips") <= 0)
        | col("total_revenue").isNull()
    ).count()

    print("\n=== VALIDATION RESULTS ===")
    print("Summary dates:", summary_dates)
    print("Reconciled trips:", total_trips)
    print("Invalid summary rows:", invalid_rows)

    assert total_trips == 491230, "Trip count mismatch!"
    assert summary_dates == 8, "Unexpected date count!"
    assert invalid_rows == 0, "Invalid summary rows found!"

    print("\nALL VALIDATION CHECKS PASSED!")

finally:
    spark.stop()
