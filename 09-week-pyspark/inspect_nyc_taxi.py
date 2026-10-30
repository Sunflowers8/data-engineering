from pathlib import Path
from pyspark.sql import SparkSession

project_root = Path(__file__).resolve().parent.parent

input_path = (
    project_root
    / "data/processed/nyc_taxi/taxi_sample_500k.parquet"
)

if not input_path.is_file():
    raise FileNotFoundError(f"Dataset not found: {input_path}")

spark = (
    SparkSession.builder
    .appName("Week9NYCTaxiInspection")
    .master("local[2]")
    .config("spark.driver.memory", "1g")
    .config("spark.sql.shuffle.partitions", "2")
    .getOrCreate()
)

try:
    spark.sparkContext.setLogLevel("ERROR")

    df = spark.read.parquet(str(input_path))

    print("\n=== DATASET SCHEMA ===")
    df.printSchema()

    print("\n=== SAMPLE RECORDS ===")
    df.show(5, truncate=False)

    print("\n=== TOTAL RECORDS ===")
    print("Total rows:", df.count())

    print("\n=== NUMBER OF PARTITIONS ===")
    print("Partitions:", df.rdd.getNumPartitions())

finally:
    spark.stop()
