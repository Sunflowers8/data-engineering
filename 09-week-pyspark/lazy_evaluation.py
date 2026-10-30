from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("Week9LazyEvaluation")
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

print("\nSTEP 1: Define a transformation")
expensive_trips = df.filter(col("fare") > 15)
print("Transformation defined.")

print("\nSTEP 2: Inspect the execution plan")
expensive_trips.explain()

print("\nSTEP 3: Trigger an action")
result = expensive_trips.count()
print(f"Trips with fares above 15: {result}")

print("\nSTEP 4: Display the result")
expensive_trips.show()

spark.stop()
