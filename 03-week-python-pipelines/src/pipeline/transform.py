import pandas as pd
def transform_taxi_data(
        df: pd.DataFrame,
        sample_size: int
        ) -> pd.DataFrame:

    # Calculate trip duration
    df["trip_duration"] = (
        df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]
    )

    df["trip_duration_minutes"] = (
        df["trip_duration"].dt.total_seconds() / 60
    )

    # Columns we want for our SQL dataset
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

    # Keep only the columns we need
    taxi_sql = df[sql_columns]

    # Keep 500,000 rows
    taxi_sample = taxi_sql.head(sample_size)

    return taxi_sample