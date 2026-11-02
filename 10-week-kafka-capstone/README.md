# Week 10 — Kafka Streaming Data Engineering Capstone

## Project Overview

A local event-driven data engineering project that simulates
taxi trips, publishes events to Apache Kafka, consumes and
validates JSON messages, and stores them in SQLite for
analytical reporting.

This project demonstrates streaming data ingestion,
event processing, replay protection, SQL analytics,
and automated data-quality testing.

## Technology Stack

- Python
- Apache Kafka 4.1.2
- Docker and Colima
- SQLite
- unittest
- JSON

## Architecture

Python Producer
      |
      v
Kafka Topic: taxi-trips
      |
      v
Python Stream Processor
      |
      v
SQLite Database
      |
      v
SQL Analytics and Validation

## Project Files

| File | Purpose |
|------|---------|
| producer.py | Publishes simulated taxi-trip events |
| consumer.py | Reads and displays Kafka messages |
| stream_processor.py | Validates and stores Kafka events in SQLite |
| test_stream_pipeline.py | Tests the eight-event sample dataset |
| validate_pipeline.py | Runs reusable data-quality checks |
| .gitignore | Excludes generated files and environments |

## Kafka Configuration

- Docker image: apache/kafka:4.1.2
- Container: kafka-week10
- Bootstrap server: localhost:9092
- Topic: taxi-trips
- Partitions: 1
- Replication factor: 1

This is a single-node local development configuration.

## Setup

Start Colima if needed:

    colima start

Start the existing Kafka container:

    docker start kafka-week10

Alternatively, create a fresh broker:

    docker run -d --name kafka-week10 \
      -p 127.0.0.1:9092:9092 apache/kafka:4.1.2

Create the topic if it does not exist:

    docker exec kafka-week10 \
      /opt/kafka/bin/kafka-topics.sh \
      --create --if-not-exists \
      --topic taxi-trips \
      --bootstrap-server localhost:9092 \
      --partitions 1 --replication-factor 1

Install the Python dependency:

    python -m pip install kafka-python

## Run the Project

From the repository root:

Publish sample events:

    python 10-week-kafka-capstone/producer.py

Read Kafka events:

    python 10-week-kafka-capstone/consumer.py

Process Kafka events into SQLite:

    python 10-week-kafka-capstone/stream_processor.py

Run the sample-specific automated tests:

    python 10-week-kafka-capstone/test_stream_pipeline.py

Run reusable data-quality validation:

    python 10-week-kafka-capstone/validate_pipeline.py

The consumer and processor stop after a period of inactivity.
They can be rerun to read retained events.

## Verified Sample Results

The original demonstration used eight Kafka events.

- Published and consumed events: 8
- Records stored in SQLite: 8
- Unique Kafka event positions: 8
- Invalid records: 0
- Total simulated fare revenue: 149.75
- Automated sample tests passed: 4/4

City revenue results:

| City | Trips | Total Fare |
|------|-------|------------|
| Pokhara | 2 | 49.00 |
| Lalitpur | 2 | 42.75 |
| Kathmandu | 3 | 40.00 |
| Bhaktapur | 1 | 18.00 |

These results are based on simulated data, not actual
NYC Taxi financial totals.

## Replay Protection

SQLite uses a composite primary key:

    (topic, partition_id, offset_id)

This prevents duplicate inserts when the same Kafka
records are replayed.

The demonstrated replay test skipped all eight
previously stored events without adding duplicates.

## Validation

The reusable validation checks:

1. Stored events are present.
2. Kafka event positions are unique.
3. No required fields are missing or invalid.
4. Total fare revenue can be calculated.

## Limitations

- Single-node Kafka broker for local development.
- Small simulated dataset rather than production traffic.
- SQLite is a lightweight local analytical destination.
- Sample-specific tests assume eight original events.
- Consumer reads existing events from the beginning.
- No persistent consumer-group offset management.
- No deployment to cloud infrastructure.
- No guarantee of end-to-end exactly-once processing.

## Learning Outcomes

- Understand Kafka topics, brokers, and partitions.
- Publish and consume events using Python.
- Decode and validate JSON events.
- Build an event-driven ingestion pipeline.
- Persist streaming records using SQLite.
- Prevent duplicate inserts during event replay.
- Query analytical results with SQL.
- Create automated tests and data-quality checks.
