
import duckdb

con = duckdb.connect(
    "data/processed/nyc_taxi/taxi_warehouse.duckdb",
    read_only=True
)

queries = {
    "Without date filter": """
        SELECT SUM(total_amount)
        FROM taxi_native
    """,
    "With date filter": """
        SELECT SUM(total_amount)
        FROM taxi_native
        WHERE pickup_date = DATE '2026-01-01'
    """
}

for name, query in queries.items():
    print(f"\n--- {name} ---")

    plan = con.execute(
        "EXPLAIN " + query
    ).fetchall()

    for row in plan:
        print(row[1])

con.close()
