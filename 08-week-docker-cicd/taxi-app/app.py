from decimal import Decimal


def calculate_revenue(trips):
    return sum(
        (Decimal(trip["fare"]) for trip in trips),
        Decimal("0.00"),
    )


def main():
    trips = [
        {"trip_id": 1, "fare": "12.50"},
        {"trip_id": 2, "fare": "18.75"},
        {"trip_id": 3, "fare": "9.25"},
        {"trip_id": 4, "fare": "20.00"},
    ]

    total_revenue = calculate_revenue(trips)

    print("NYC Taxi Revenue Report")
    print(f"Total trips: {len(trips)}")
    print(f"Total revenue: ${total_revenue:.2f}")


if __name__ == "__main__":
    main()
