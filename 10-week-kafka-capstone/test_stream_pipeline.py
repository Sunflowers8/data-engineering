import sqlite3
import unittest
from pathlib import Path

DB_PATH = (
    Path(__file__).resolve().parent
    / "data/taxi_stream.db"
)


class TestKafkaStreamPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not DB_PATH.is_file():
            raise FileNotFoundError(
                "Run stream_processor.py before testing."
            )

        cls.connection = sqlite3.connect(
            f"{DB_PATH.as_uri()}?mode=ro",
            uri=True,
        )

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "connection"):
            cls.connection.close()

    def test_total_records(self):
        count = self.connection.execute(
            "SELECT COUNT(*) FROM taxi_trips"
        ).fetchone()[0]

        self.assertEqual(count, 8)

    def test_total_revenue(self):
        revenue = self.connection.execute(
            "SELECT ROUND(SUM(fare), 2) FROM taxi_trips"
        ).fetchone()[0]

        self.assertAlmostEqual(revenue, 149.75, places=2)

    def test_no_duplicate_kafka_offsets(self):
        duplicates = self.connection.execute("""
            SELECT COUNT(*) FROM (
                SELECT topic, partition_id, offset_id
                FROM taxi_trips
                GROUP BY topic, partition_id, offset_id
                HAVING COUNT(*) > 1
            )
        """).fetchone()[0]

        self.assertEqual(duplicates, 0)

    def test_valid_fares(self):
        invalid = self.connection.execute("""
            SELECT COUNT(*) FROM taxi_trips
            WHERE fare < 0 OR fare IS NULL
        """).fetchone()[0]

        self.assertEqual(invalid, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
