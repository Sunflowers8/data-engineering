import pandas as pd

file_path = "data/raw/nyc_taxi/taxi_zone_lookup.csv"

df = pd.read_csv(file_path)

print(df.head())

df.info()

print(df.describe())
print(df.columns)
print(df.shape)
print(df.isnull().sum())

print(df['Zone'].value_counts())
print(df['Borough'].value_counts())