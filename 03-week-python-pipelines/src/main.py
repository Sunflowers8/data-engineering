from pipeline.extract import extract_parquet
from pipeline.transform import transform_taxi_data
from pipeline.load import load_to_csv, load_to_postgres
from pipeline.config import PipelineConfig
from pipeline.database import DatabaseClient

config = PipelineConfig(
    input_path="data/raw/nyc_taxi/yellow_tripdata_2026-01.parquet",
    output_path="data/processed/nyc_taxi/taxi_sample_500k.csv",
    sample_size=500000
)

df = extract_parquet(config.input_path)
df = transform_taxi_data(df, config.sample_size)

database_url = "postgresql+psycopg2://menuka@localhost/employee_db"

db = DatabaseClient(database_url)
engine = db.get_engine()

load_to_csv(df, config.output_path)
load_to_postgres(df.head(100), engine, "taxi_trips_pipeline")

