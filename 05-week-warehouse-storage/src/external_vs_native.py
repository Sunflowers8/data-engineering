
from pathlib import Path
import duckdb

# Existing partitioned Parquet dataset
parquet_path = (
    "data/processed/nyc_taxi/partitioned/*/*.parquet"
)

# Local DuckDB database (not for GitHub)
db_path = Path(
    "data/processed/nyc_taxi/taxi_warehouse.duckdb"
)

con = duckdb.connect(str(db_path))

# 1. Create a VIEW over external Parquet files
con.execute(f"""
    CREATE OR REPLACE VIEW taxi_external AS
    SELECT *
    FROM read_parquet(
        '{parquet_path}',
        hive_partitioning = true
    )
""")

# 2. Query the external files
external_count = con.execute("""
    SELECT COUNT(*)
    FROM taxi_external
    WHERE pickup_date = DATE '2026-01-01'
""").fetchone()[0]

print("External January 1 rows:", external_count)

# 3. Load files into a native DuckDB table
con.execute("""
    CREATE OR REPLACE TABLE taxi_native AS
    SELECT * FROM taxi_external
""")

# 4. Query the native table
native_count = con.execute("""
    SELECT COUNT(*)
    FROM taxi_native
    WHERE pickup_date = DATE '2026-01-01'
""").fetchone()[0]

print("Native January 1 rows:", native_count)

# 5. Verify that both results match
assert external_count == native_count
print("Validation passed: row counts match!")

con.close()
