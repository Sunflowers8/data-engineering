import json
import sqlite3
from pathlib import Path

from kafka import KafkaConsumer

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "taxi_stream.db"

connection = sqlite3.connect(DB_PATH)

connection.execute("""
CREATE TABLE IF NOT EXISTS taxi_trips (
    topic TEXT NOT NULL,
    partition_id INTEGER NOT NULL,
    offset_id INTEGER NOT NULL,
    trip_id INTEGER NOT NULL,
    pickup TEXT NOT NULL,
    fare REAL NOT NULL,
    PRIMARY KEY (topic, partition_id, offset_id)
)
""")

connection.commit()

consumer = KafkaConsumer(
    "taxi-trips",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    group_id=None,
    consumer_timeout_ms=5000,
)

processed = 0
skipped = 0
invalid = 0

print("\n=== KAFKA STREAM PROCESSOR ===")

try:
    for message in consumer:
        try:
            trip = json.loads(message.value.decode("utf-8"))

            trip_id = trip["trip_id"]
            pickup = trip["pickup"]
            fare = trip["fare"]

            if (
                type(trip_id) is not int
                or type(pickup) is not str
                or not pickup.strip()
                or type(fare) not in (int, float)
                or not (0 <= fare < float("inf"))
            ):
                raise ValueError("Invalid taxi event")

            cursor = connection.execute(
                """
                INSERT OR IGNORE INTO taxi_trips
                (topic, partition_id, offset_id,
                 trip_id, pickup, fare)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    message.topic,
                    message.partition,
                    message.offset,
                    trip_id,
                    pickup,
                    fare,
                ),
            )

            connection.commit()

            if cursor.rowcount == 1:
                processed += 1
                print(
                    f"Stored trip {trip_id} "
                    f"from {pickup}: {fare}"
                )
            else:
                skipped += 1

        except (ValueError, KeyError, TypeError,
                UnicodeDecodeError, json.JSONDecodeError):
            invalid += 1
            print(
                f"Invalid event at offset {message.offset}"
            )

finally:
    consumer.close()
    connection.close()

print("\n=== PROCESSING RESULTS ===")
print("New records stored:", processed)
print("Duplicates skipped:", skipped)
print("Invalid events:", invalid)
print("Database:", DB_PATH)
