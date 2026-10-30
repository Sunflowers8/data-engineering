from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("Week9TaxiPartitions")
    .master("local[2]")
    .config("spark.driver.memory", "1g")
    .config("spark.sql.shuffle.partitions", "2")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

trips = [(i, float(i * 5)) for i in range(1, 9)]

df = spark.createDataFrame(trips, ["trip_id", "fare"])

print("\n=== ORIGINAL PARTITIONS ===")
print("Partition count:", df.rdd.getNumPartitions())

print("\n=== REPARTITION INTO TWO ===")
two_partitions = df.repartition(2)
print("Partition count:", two_partitions.rdd.getNumPartitions())

print("\n=== RECORDS PER PARTITION ===")
partition_sizes = two_partitions.rdd.mapPartitions(
    lambda rows: [sum(1 for _ in rows)]
).collect()

for index, size in enumerate(partition_sizes):
    print(f"Partition {index}: {size} records")

print("\n=== TOTAL RECORDS ===")
print("Total:", two_partitions.count())

spark.stop()