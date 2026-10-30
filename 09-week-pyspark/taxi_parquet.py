from pathlib import Path
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("Week9TaxiParquet")
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

output_path = Path(
    "09-week-pyspark/data/taxi_parquet"
).resolve()

output_path.parent.mkdir(parents=True, exist_ok=True)

print("\n=== WRITE PARQUET ===")
df.write.mode("overwrite").parquet(str(output_path))
print("Saved to:", output_path)

print("\n=== READ PARQUET ===")
loaded_df = spark.read.parquet(str(output_path))
loaded_df.orderBy("trip_id").show()

print("\n=== VERIFY RECORD COUNT ===")
print("Original:", df.count())
print("Loaded:", loaded_df.count())

spark.stop()
