import pandas as pd
from sqlalchemy import create_engine

file_path = "data/raw/nyc_taxi/taxi_zone_lookup.csv"

df = pd.read_csv(file_path)

df = df.rename(columns={
    "LocationID": "location_id",
    "Borough": "borough",
    "Zone": "zone"
})

df = df.fillna({
    "borough": "Unknown",
    "zone": "Unknown",
    "service_zone": "Unknown"
})

print(df.head())
print(df.isnull().sum())

database_url = "postgresql+psycopg2://menuka@localhost/employee_db"

engine = create_engine(database_url)

df.to_sql(
    "dim_location",
    engine,
    if_exists="append",
    index=False
)