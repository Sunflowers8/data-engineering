
import duckdb
import statistics
import time

DB_PATH = "data/processed/nyc_taxi/taxi_warehouse.duckdb"

con = duckdb.connect(DB_PATH, read_only=True)

queries = {
    "External Parquet": """
        SELECT COUNT(*), SUM(total_amount)
        FROM taxi_external
        WHERE pickup_date = DATE '2026-01-01'
    """,
    "Native DuckDB": """
        SELECT COUNT(*), SUM(total_amount)
        FROM taxi_native
        WHERE pickup_date = DATE '2026-01-01'
    """
}

for name, sql in queries.items():
    # Warm-up execution
    con.execute(sql).fetchone()

    times = []

    for _ in range(5):
        start = time.perf_counter()
        result = con.execute(sql).fetchone()
        elapsed = time.perf_counter() - start
        times.append(elapsed)

    print(f"\n{name}")
    print(f"Rows: {result[0]:,}")
    print(f"Revenue: ${result[1]:,.2f}")
    print(f"Median query time: {statistics.median(times):.5f} seconds")

con.close()
