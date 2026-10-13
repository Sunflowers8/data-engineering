
from pathlib import Path
import pandas as pd

source = Path("data/processed/nyc_taxi/taxi_sample_500k.csv")
destination = Path("data/processed/nyc_taxi/partitioned")

# Read sample data
df = pd.read_csv(source)

# Convert pickup datetime
df["tpep_pickup_datetime"] = pd.to_datetime(
    df["tpep_pickup_datetime"],
    errors="coerce"
)

# Remove rows with invalid dates
df = df.dropna(subset=["tpep_pickup_datetime"]).copy()

# Create partition column
df["pickup_date"] = df[
    "tpep_pickup_datetime"
].dt.strftime("%Y-%m-%d")

# Write partitioned Parquet files
df.to_parquet(
    destination,
    engine="pyarrow",
    partition_cols=["pickup_date"],
    index=False
)

print("Partitioned dataset created!")
print(f"Rows written: {len(df):,}")
print(f"Output directory: {destination}")
