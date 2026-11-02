import json
import time
from datetime import datetime, timezone

from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(
        value
    ).encode("utf-8"),
)

taxi_trips = [
    {"trip_id": 101, "pickup": "Kathmandu", "fare": 15.50},
    {"trip_id": 102, "pickup": "Lalitpur", "fare": 22.75},
    {"trip_id": 103, "pickup": "Bhaktapur", "fare": 18.00},
    {"trip_id": 104, "pickup": "Pokhara", "fare": 30.25},
    {"trip_id": 105, "pickup": "Kathmandu", "fare": 12.00},
]

try:
    print("\n=== PYTHON KAFKA PRODUCER ===")

    for trip in taxi_trips:
        trip["event_time"] = datetime.now(
            timezone.utc
        ).isoformat()

        future = producer.send(
            "taxi-trips",
            value=trip,
        )

        metadata = future.get(timeout=10)

        print(
            f"Sent Trip {trip['trip_id']} | "
            f"Pickup: {trip['pickup']} | "
            f"Fare: {trip['fare']} | "
            f"Offset: {metadata.offset}"
        )

        time.sleep(1)

    producer.flush()
    print("\nAll 5 taxi events published successfully!")

finally:
    producer.close()
