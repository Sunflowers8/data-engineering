import json

from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "taxi-trips",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    group_id=None,
    consumer_timeout_ms=10000,
    value_deserializer=lambda value: json.loads(
        value.decode("utf-8")
    ),
)

print("\n=== PYTHON KAFKA CONSUMER ===")

count = 0

try:
    for message in consumer:
        trip = message.value

        print(
            f"Trip ID: {trip['trip_id']} | "
            f"Pickup: {trip['pickup']} | "
            f"Fare: {trip['fare']}"
        )

        count += 1

finally:
    consumer.close()

print(f"\nTotal events consumed: {count}")
