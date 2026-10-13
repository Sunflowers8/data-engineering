
import pandas as pd
from pathlib import Path
import time

# File paths
csv_path = Path("data/processed/nyc_taxi/taxi_sample_500k.csv")
parquet_path = Path("data/processed/nyc_taxi/taxi_sample_500k.parquet")

# Step 1: Read CSV
df = pd.read_csv(csv_path)

# Step 2: Convert to Parquet
df.to_parquet(parquet_path, engine="pyarrow", index=False)

# Step 3: Compare file sizes
csv_mb = csv_path.stat().st_size / (1024 ** 2)
parquet_mb = parquet_path.stat().st_size / (1024 ** 2)

print(f"CSV size: {csv_mb:.2f} MB")
print(f"Parquet size: {parquet_mb:.2f} MB")
print(f"Space saved: {(1 - parquet_mb / csv_mb) * 100:.2f}%")

# Step 4: Compare reading three columns
columns = ["trip_distance", "fare_amount", "total_amount"]

start = time.perf_counter()
csv_data = pd.read_csv(csv_path, usecols=columns)
csv_time = time.perf_counter() - start

start = time.perf_counter()
parquet_data = pd.read_parquet(parquet_path, columns=columns)
parquet_time = time.perf_counter() - start

print(f"CSV read time: {csv_time:.4f} seconds")
print(f"Parquet read time: {parquet_time:.4f} seconds")
print(f"Rows compared: {len(csv_data):,}")

