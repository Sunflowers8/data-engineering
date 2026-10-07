import pandas as pd

file_path = "data/raw/nyc_taxi/yellow_tripdata_2026-01.parquet"

df = pd.read_parquet(file_path)

df = df.rename(columns={
    "tpep_pickup_datetime": "pickup_datetime",
    "tpep_dropoff_datetime": "dropoff_datetime",
   