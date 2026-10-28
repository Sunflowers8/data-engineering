import unittest
from decimal import Decimal

from app import calculate_revenue


class TestTaxiRevenue(unittest.TestCase):

    def test_four_taxi_trips(self):
        trips = [
            {"fare": "12.50"},
            {"fare": "18.75"},
            {"fare": "9.25"},
            {"fare": "20.00"},
        ]
        self.assertEqual(
            calculate_revenue(trips),
            Decimal("60.50"),
        )

    def test_empty_trips(self):
        self.assertEqual(
            calculate_revenue([]),
            Decimal("0.00"),
        )

    def test_decimal_precision(self):
        trips = [
            {"fare": "0.10"},
            {"fare": "0.20"},
        ]
        self.assertEqual(
            calculate_revenue(trips),
            Decimal("0.30"),
        )


if __name__ == "__main__":
    unittest.main()
