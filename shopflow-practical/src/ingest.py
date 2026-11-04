
import argparse
import csv
import hashlib
import json
import logging
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

import duckdb


ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "raw"
DB_PATH = ROOT / "shopflow.duckdb"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

SCHEMAS = {
    "customers": {
        "required": ["source_seq", "customer_id", "updated_at"],
        "fields": ["customer_id", "full_name", "email", "city"],
        "timestamps": ["updated_at"],
        "amounts": [],
        "key": "customer_id",
    },
    "orders": {
        "required": [
            "source_seq", "order_id", "customer_id",
            "order_ts", "status", "total_amount", "updated_at"
        ],
        "fields": ["order_id", "customer_id", "status"],
        "timestamps": ["order_ts", "updated_at"],
        "amounts": ["total_amount"],
        "key": "order_id",
    },
    "payments": {
        "required": [
            "source_seq", "payment_id", "order_id",
            "payment_ts", "amount", "status", "updated_at"
        ],
        "fields": ["payment_id", "order_id", "method", "status"],
        "timestamps": ["payment_ts", "updated_at"],
        "amounts": ["amount"],
        "key": "payment_id",
    },
}

COLUMNS = {
    "customers": [
        "customer_id", "full_name", "email",
        "city", "updated_at", "source_seq"
    ],
    "orders": [
        "order_id", "customer_id", "order_ts",
        "status", "total_amount", "updated_at", "source_seq"
    ],
    "payments": [
        "payment_id", "order_id", "payment_ts",
        "amount", "method", "status", "updated_at", "source_seq"
    ],
}


def parse_timestamp(value):
    value = str(value).strip().replace("Z", "+00:00")
    result = datetime.fromisoformat(value)

    if result.tzinfo is None:
        raise ValueError("Timestamp must include a timezone")

    return result.astimezone(timezone.utc)


def parse_amount(value):
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError):
        raise ValueError("Invalid numeric amount")

    if not amount.is_finite() or amount < 0:
        raise ValueError("Amount must be finite and non-negative")

    return amount.quantize(Decimal("0.01"))


def read_source(folder, source):
    filename = (
        "payments.json" if source == "payments"
        else f"{source}.csv"
    )
    path = folder / filename

    if source == "payments":
        with path.open("r", encoding="utf-8") as file:
            records = json.load(file)

        if not isinstance(records, list):
            raise ValueError(f"{path}: expected a JSON list")
    else:
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                raise ValueError(f"{path}: missing CSV header")

            missing = (
                set(SCHEMAS[source]["required"])
                - set(reader.fieldnames)
            )

            if missing:
                raise ValueError(
                    f"{path}: missing columns {sorted(missing)}"
                )

            records = list(reader)

    for record in records:
        if not isinstance(record, dict):
            raise ValueError(f"{path}: expected object records")

    logging.info("%s: received %d rows", source, len(records))
    return records


def validate_record(record, source):
    schema = SCHEMAS[source]

    missing = [
        field for field in schema["required"]
        if not str(record.get(field) or "").strip()
    ]

    if missing:
        raise ValueError(
            "Missing required fields: " + ", ".join(missing)
        )

    clean = {}

    try:
        clean["source_seq"] = int(record["source_seq"])
    except (ValueError, TypeError):
        raise ValueError("Invalid source_seq")

    for field in schema["fields"]:
        value = record.get(field)
        clean[field] = str(value).strip() if value is not None else ""

    for field in schema["timestamps"]:
        try:
            clean[field] = parse_timestamp(record[field])
        except (ValueError, TypeError):
            raise ValueError(f"Invalid timestamp: {field}")

    for field in schema["amounts"]:
        clean[field] = parse_amount(record[field])

    if source == "orders":
        if clean["status"] not in {
            "pending", "completed", "cancelled"
        }:
            raise ValueError("Invalid order status")

    if source == "payments":
        if clean["status"] not in {
            "initiated", "failed", "captured", "refunded"
        }:
            raise ValueError("Invalid payment status")

    return clean


def create_tables(db):
    db.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id VARCHAR PRIMARY KEY,
            full_name VARCHAR,
            email VARCHAR,
            city VARCHAR,
            updated_at TIMESTAMPTZ,
            source_seq BIGINT
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id VARCHAR PRIMARY KEY,
            customer_id VARCHAR,
            order_ts TIMESTAMPTZ,
            status VARCHAR,
            total_amount DECIMAL(18, 2),
            updated_at TIMESTAMPTZ,
            source_seq BIGINT
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            payment_id VARCHAR PRIMARY KEY,
            order_id VARCHAR,
            payment_ts TIMESTAMPTZ,
            amount DECIMAL(18, 2),
            method VARCHAR,
            status VARCHAR,
            updated_at TIMESTAMPTZ,
            source_seq BIGINT
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS watermarks (
            source_name VARCHAR PRIMARY KEY,
            last_updated_at TIMESTAMPTZ,
            last_source_seq BIGINT
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS rejected_rows (
            reject_id VARCHAR PRIMARY KEY,
            batch_date VARCHAR,
            source_name VARCHAR,
            reason VARCHAR,
            raw_record VARCHAR
        )
    """)


def get_watermark(db, source):
    result = db.execute("""
        SELECT last_updated_at, last_source_seq
        FROM watermarks
        WHERE source_name = ?
    """, [source]).fetchone()

    return result


def save_rejection(db, batch_date, source, record, reason):
    raw_json = json.dumps(
        record, sort_keys=True, default=str
    )

    reject_id = hashlib.sha256(
        f"{batch_date}:{source}:{raw_json}:{reason}".encode()
    ).hexdigest()

    db.execute("""
        INSERT INTO rejected_rows
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT (reject_id) DO NOTHING
    """, [reject_id, batch_date, source, reason, raw_json])


def upsert_record(db, source, record):
    columns = COLUMNS[source]
    column_sql = ", ".join(columns)
    placeholders = ", ".join(["?"] * len(columns))

    update_sql = ", ".join(
        f"{col} = excluded.{col}"
        for col in columns
        if col != SCHEMAS[source]["key"]
    )

    key = SCHEMAS[source]["key"]

    query = f"""
        INSERT INTO {source} ({column_sql})
        VALUES ({placeholders})
        ON CONFLICT ({key}) DO UPDATE SET
            {update_sql}
        WHERE
            excluded.updated_at > {source}.updated_at
            OR (
                excluded.updated_at = {source}.updated_at
                AND excluded.source_seq > {source}.source_seq
            )
    """

    db.execute(query, [record[col] for col in columns])


def save_watermark(db, source, timestamp, sequence):
    db.execute("""
        INSERT INTO watermarks
        VALUES (?, ?, ?)
        ON CONFLICT (source_name) DO UPDATE SET
            last_updated_at = excluded.last_updated_at,
            last_source_seq = excluded.last_source_seq
    """, [source, timestamp, sequence])


def process_source(db, folder, batch_date, source, backfill):
    records = read_source(folder, source)
    latest = {}
    rejected = 0

    for record in records:
        try:
            clean = validate_record(record, source)
            key = clean[SCHEMAS[source]["key"]]

            previous = latest.get(key)

            version = (
                clean["updated_at"],
                clean["source_seq"]
            )

            if previous is None or version > (
                previous["updated_at"],
                previous["source_seq"]
            ):
                latest[key] = clean

        except (ValueError, TypeError, KeyError) as error:
            save_rejection(
                db, batch_date, source, record, str(error)
            )
            rejected += 1

    watermark = get_watermark(db, source)
    processed = 0
    newest = watermark

    for record in sorted(
        latest.values(),
        key=lambda r: (r["updated_at"], r["source_seq"])
    ):
        version = (
            record["updated_at"],
            record["source_seq"]
        )

        if not backfill and watermark and version <= watermark:
            continue

        upsert_record(db, source, record)
        processed += 1

        if newest is None or version > newest:
            newest = version

    if newest and (watermark is None or newest > watermark):
        save_watermark(db, source, newest[0], newest[1])

    logging.info(
        "%s: %d valid unique, %d rejected, %d processed",
        source, len(latest), rejected, processed
    )


def process_batch(db, batch_date, backfill=False):
    folder = RAW_DIR / batch_date

    if not folder.is_dir():
        raise FileNotFoundError(f"Batch not found: {folder}")

    logging.info("Starting batch: %s", batch_date)

    db.execute("BEGIN TRANSACTION")

    try:
        for source in ("customers", "orders", "payments"):
            process_source(
                db, folder, batch_date, source, backfill
            )

        db.execute("COMMIT")
        logging.info("Batch committed successfully")

    except Exception:
        db.execute("ROLLBACK")
        logging.exception("Batch failed; changes rolled back")
        raise


def print_summary(db):
    logging.info("Current warehouse record counts:")

    for source in ("customers", "orders", "payments"):
        count = db.execute(
            f"SELECT COUNT(*) FROM {source}"
        ).fetchone()[0]

        logging.info("%s: %d", source, count)

    rejected = db.execute(
        "SELECT COUNT(*) FROM rejected_rows"
    ).fetchone()[0]

    logging.info("Quarantined rows: %d", rejected)



def main():
    parser = argparse.ArgumentParser(
        description="ShopFlow batch ingestion"
    )

    parser.add_argument(
        "--batch-date",
        help="Process only this batch (YYYY-MM-DD)"
    )

    parser.add_argument(
        "--backfill",
        action="store_true",
        help="Reprocess a historical batch safely"
    )

    args = parser.parse_args()

    if args.batch_date:
        batches = [args.batch_date]
    else:
        batches = sorted(
            folder.name
            for folder in RAW_DIR.iterdir()
            if folder.is_dir()
        )

    if not batches:
        raise ValueError("No input batches found")

    db = duckdb.connect(str(DB_PATH))

    try:
        create_tables(db)

        for batch in batches:
            process_batch(db, batch, args.backfill)

        print_summary(db)

    finally:
        db.close()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("ShopFlow ingestion failed")
        raise SystemExit(1)
