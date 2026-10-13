
import pandas as pd
from pathlib import Path

dataset_path = Path(
    "data/processed/nyc_taxi/partitioned"
)

df = pd.read_parquet(
    dataset_path,
    filters=[
        ("pickup_date", "==", "2026-01-01")
    ],
    engine="pyarrow"
)

print("Rows for January 1:", len(df))
print(df[[
    "pickup_date",
    "trip_distance",
    "total_amount"
]].head())
