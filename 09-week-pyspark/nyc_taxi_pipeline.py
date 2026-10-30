from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    avg,
    col,
    count,
    round as spark_round,
    sum as spark_sum,
    to_date,
    to_timestamp,
)

project_root = Path(__file__).resolve().parent.parent

source_path = (
    project_root
    / "data/processed/nyc_taxi/taxi_sample_500k.parquet"
)

output_path = (
    project_root
    / "09-week-pyspark/data/daily_taxi_summary"
)

if not source_path.is_file():
    raise FileNotFoundError(f"Missing source: {source_path}")

spark = (
    SparkSession.builder
    .appName("Week9NYCTaxiAnalytics")
    .master("local[2]")
    .config("spark.driver.memory", "1g")
    .config("spark.sql.shuffle.partitions", "2")
    .getOrCreate()
)

try:
    spark.sparkContext.setLogLevel("ERROR")

    print("\n=== STEP 1: READ SOURCE ===")
    df = spark.read.parquet(str(source_path))
    print("Source records:", df.count())

    print("\n=== STEP 2: CLEAN DATA ===")
    cleaned_df = (
        df.withColumn(
            "pickup_timestamp",
            to_timestamp(
                col("tpep_pickup_datetime"),
                "yyyy-MM-dd HH:mm:ss",
            ),
        )
        .withColumn(
            "pickup_date",
            to_date(col("pickup_timestamp")),
        )
        .filter(col("pickup_date").isNotNull())
        .filter(col("total_amount").isNotNull())
        .filter(col("total_amount") >= 0)
        .filter(col("trip_distance").isNotNull())
        .filter(col("trip_distance") >= 0)
    )

    print("Valid records:", cleaned_df.count())

    print("\n=== STEP 3: AGGREGATE BY DATE ===")
    daily_summary = (
        cleaned_df.groupBy("pickup_date")
        .agg(
            count("*").alias("total_trips"),
            spark_round(
                spark_sum("total_amount"), 2
            ).alias("total_revenue"),
            spark_round(
                avg("total_amount"), 2
            ).alias("average_trip_amount"),
            spark_round(
                avg("trip_distance"), 2
            ).alias("average_distance"),
        )
        .orderBy("pickup_date")
    )

    daily_summary.show(15, truncate=False)

    print("\n=== STEP 4: SAVE PARQUET ===")
    daily_summary.write.mode("overwrite").parquet(
        str(output_path)
    )

    print("Saved output:", output_path)

    print("\n=== STEP 5: VERIFY OUTPUT ===")
    verified_df = spark.read.parquet(str(output_path))

    print("Summary dates:", verified_df.count())
    verified_df.orderBy("pickup_date").show(5)

    print("\nPIPELINE COMPLETED SUCCESSFULLY")

finally:
    spark.stop()
