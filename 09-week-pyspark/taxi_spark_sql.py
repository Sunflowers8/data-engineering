from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("Week9SparkSQL")
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

df = spark.createDataFrame(
    trips,
    ["trip_id", "city", "fare"]
)

# Make the DataFrame available to Spark SQL.
df.createOrReplaceTempView("taxi_trips")

print("\n=== SPARK SQL: ALL TRIPS ===")

spark.sql("""
    SELECT *
    FROM taxi_trips
    ORDER BY trip_id
""").show()

print("\n=== SPARK SQL: REVENUE BY CITY ===")

spark.sql("""
    SELECT
        city,
        COUNT(*) AS total_trips,
        ROUND(SUM(fare), 2) AS total_revenue,
        ROUND(AVG(fare), 2) AS average_fare
    FROM taxi_trips
    GROUP BY city
    ORDER BY total_revenue DESC
""").show()

spark.stop()
