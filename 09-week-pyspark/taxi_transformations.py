from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round as spark_round

spark = (
    SparkSession.builder
    .appName("Week9TaxiTransformations")
    .master("local[2]")
    .config("spark.driver.memory", "1g")
    .config("spark.sql.shuffle.partitions", "2")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

trips = [
    (1, "Kathmandu", 12.50, 2.0),
    (2, "Pokhara", 18.75, 5.0),
    (3, "Kathmandu", 9.25, 1.5),
    (4, "Lalitpur", 20.00, 4.0),
]

df = spark.createDataFrame(
    trips,
    ["trip_id", "city", "fare", "distance_km"]
)

print("\n=== ORIGINAL DATA ===")
df.show()

print("\n=== SELECT COLUMNS ===")
df.select("city", "fare").show()

print("\n=== FILTER FARES ABOVE 15 ===")
df.filter(col("fare") > 15).show()

print("\n=== CREATE FARE PER KM ===")
df.withColumn(
    "fare_per_km",
    spark_round(col("fare") / col("distance_km"), 2)
).show()

spark.stop()
