from pyspark.sql import SparkSession
spark = (
SparkSession.builder
.appName("Week9FirstSpark")
.master("local[2]")
.config("spark.driver.memory", "1g")
.config("spark.sql.shuffle.partitions", "2")
.getOrCreate()
)
trips = [
(1, 12.50),
(2, 18.75),
(3, 9.25),
(4, 20.00),
]
df = spark.createDataFrame(
trips,
["trip_id", "fare"]
)
print ("\n== FIRST SPARK DATAFRAME ===")
df.show()
print ("Total rows: ", df.count())
spark.stop()
