import pandas as pd

file_path = "data/raw/nyc_taxi/yellow_tripdata_2026-01.parquet"

df = pd.read_parquet(file_path)

print(df.head())
print (df.shape)
print(df.columns)
print (df.dtypes)
print(df.isnull().sum())
print("NULL percentage: ",(df.isnull().sum()/(len(df))*100))
both_missing = df[
    (df["passenger_count"].isnull()) &
    (df["RatecodeID"].isnull())
]
print(len(both_missing))
print(both_missing["payment_type"].value_counts())

all_missing = df [
    (df["passenger_count"].isnull()) &
    (df["RatecodeID"].isnull()) &
    (df["store_and_fwd_flag"].isnull()) &
    (df["congestion_surcharge"].isnull()) &
    (df["Airport_fee"].isnull())
]
print(len(all_missing))

print("Duplicate rows:",df.duplicated().sum())



invalid_distance = df[
 df ["trip_distance"] <= 0 
]
print("Trips with distance <= :",len(invalid_distance))

negative_distance = df[
 df ["trip_distance"] < 0
]
print("Trips with negative distance:", len(negative_distance))

negative_fare = df [
    df ["fare_amount"] < 0
]
print ("Trips with negative fare:", len(negative_fare))

invalid_time = df [
    df["tpep_pickup_datetime"] > df["tpep_dropoff_datetime"]
]
print("Drop-off before pickup:", len(invalid_time))

same_time = df [
    df["tpep_pickup_datetime"] == df["tpep_dropoff_datetime"]
]
print("Pickup and drop-off at same time:", len(same_time))

df["trip_duration"] = df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]


print(
    df[
        ["tpep_pickup_datetime",
         "tpep_dropoff_datetime",
         "trip_duration"]
    ].head()
)

df["trip_duration_minutes"] = (
    df["trip_duration"].dt.total_seconds() / 60
)
print(
    df[
        ["tpep_pickup_datetime",
         "tpep_dropoff_datetime",
         "trip_duration_minutes"]
    ].head()
)

sql_columns = [
    "VendorID",
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "RatecodeID",
    "store_and_fwd_flag",
    "PULocationID",
    "DOLocationID",
    "payment_type",
    "fare_amount",
    "extra",
    "mta_tax",
    "tip_amount",
    "tolls_amount",
    "improvement_surcharge",
    "total_amount",
    "congestion_surcharge",
    "Airport_fee",
    "cbd_congestion_fee",
    "trip_duration_minutes"
]
taxi_sql = df[sql_columns]
taxi_sample = taxi_sql.head(500000)

print(taxi_sample.shape)

output_path = "data/processed/nyc_taxi/taxi_sample_500k.csv"

taxi_sample.to_csv(
    output_path,
    index=False
)

print("Saved:", output_path)