
from pathlib import Path
import duckdb

# Load local credentials
env_path = Path("05-week-warehouse-storage/.env.minio")
credentials = {}

for line in env_path.read_text().splitlines():
    if "=" in line and not line.startswith("#"):
        key, value = line.split("=", 1)
        credentials[key.strip()] = value.strip()

# Escape values before putting them into SQL
def sql_string(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"

access_key = sql_string(credentials["MINIO_ROOT_USER"])
secret_key = sql_string(credentials["MINIO_ROOT_PASSWORD"])

con = duckdb.connect()

# Enable reading from S3-compatible storage
con.execute("INSTALL httpfs")
con.execute("LOAD httpfs")

# Temporary credentials for this session only
con.execute(f"""
    CREATE OR REPLACE TEMPORARY SECRET minio_secret (
        TYPE s3,
        KEY_ID {access_key},
        SECRET {secret_key},
        REGION 'us-east-1',
        ENDPOINT '127.0.0.1:9000',
        URL_STYLE 'path',
        USE_SSL false
    )
""")

# Read Parquet objects directly from MinIO
s3_path = (
    "s3://nyc-taxi-data/processed/*/*.parquet"
)

con.execute(f"""
    CREATE VIEW taxi_s3 AS
    SELECT *
    FROM read_parquet(
        '{s3_path}',
        hive_partitioning = true
    )
""")

# Validate all records
total_rows = con.execute("""
    SELECT COUNT(*) FROM taxi_s3
""").fetchone()[0]

print(f"Total S3 records: {total_rows:,}")

# Query January 1
result = con.execute("""
    SELECT
        COUNT(*) AS trip_count,
        SUM(total_amount) AS revenue
    FROM taxi_s3
    WHERE pickup_date = DATE '2026-01-01'
""").fetchone()

print(f"January 1 trips: {result[0]:,}")
print(f"January 1 revenue: ${result[1]:,.2f}")

assert total_rows == 500_000
assert result[0] == 66_984

print("S3 query validation passed!")

con.close()
