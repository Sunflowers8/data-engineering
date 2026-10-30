from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, count, round as spark_round, sum as spark_sum

spark = (
    SparkSession.builder
    .appName("Week9TaxiAggregations")
    .master("local[2]")
    .config("spark.driver.memory", "1g")
    .config("spark.sql.shuffle.partitions", "2")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

trips = [
    (1, "Kathmandu", 12.50),
    (2, "Pokhara", 18.75),
    (3, "Kathmandu", 9.25),
    (4, "Lalitpur", 20.00),
]

df = spark.createDataFrame(trips, ["trip_id", "city", "fare"])

print("\n=== REVENUE BY CITY ===")

revenue_by_city = (
    df.groupBy("city")
    .agg(
        count("*").alias("total_trips"),
        spark_round(spark_sum("fare"), 2).alias("total_revenue"),
        spark_round(avg("fare"), 2).alias("average_fare"),
    )
    .orderBy(col("total_revenue").desc())
)

revenue_by_city.show()

spark.stop()
