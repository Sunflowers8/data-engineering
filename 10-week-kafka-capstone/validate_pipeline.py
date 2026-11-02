import sqlite3
from pathlib import Path

db_path = (
    Path(__file__).resolve().parent
    / "data/taxi_stream.db"
)

if not db_path.is_file():
    raise FileNotFoundError(
        "Database not found. Run stream_processor.py first."
    )

connection = sqlite3.connect(
    f"{db_path.as_uri()}?mode=ro",
    uri=True,
)

try:
    total, unique, invalid, revenue = (
        connection.execute("""
            SELECT
                COUNT(*),
                COUNT(DISTINCT
                    topic || ':' ||
                    partition_id || ':' ||
                    offset_id
                ),
                SUM(
                    CASE
                        WHEN trip_id IS NULL
                          OR pickup IS NULL
                          OR TRIM(pickup) = ''
                          OR fare IS NULL
                          OR fare < 0
                        THEN 1
                        ELSE 0
                    END
                ),
                ROUND(SUM(fare), 2)
            FROM taxi_trips
        """).fetchone()
    )

    print("\n=== CAPSTONE VALIDATION ===")
    print("Stored events:", total)
    print("Unique Kafka offsets:", unique)
    print("Invalid records:", invalid)
    print("Total fare revenue:", revenue)

    assert total > 0, "Database contains no events"
    assert total == unique, "Duplicate Kafka offsets found"
    assert invalid == 0, "Invalid records found"

    print("\nALL DATA-QUALITY CHECKS PASSED!")

finally:
    connection.close()
