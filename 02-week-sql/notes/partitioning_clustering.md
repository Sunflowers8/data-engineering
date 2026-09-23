# Partitioning and Clustering

## Overview

Partitioning is a database design technique that divides a large logical table into smaller physical sections.

During Week 2, PostgreSQL range partitioning was practiced using a real **500,000-row NYC Yellow Taxi dataset**.

The partition key used was:

```text
pickup_datetime
```

This is appropriate for trip data because large analytical datasets are commonly queried by time period.

---

# Why Partition Data?

Imagine storing several years of taxi trips in one very large table.

A query may only need:

```text
February 2026
```

Without useful physical organization, the database may need to consider a much larger amount of data.

With monthly partitions:

```text
taxi_trips
│
├── 2026-01
├── 2026-02
├── 2026-03
├── 2026-04
└── ...
```

PostgreSQL can potentially eliminate irrelevant partitions.

---

# Range Partitioning

The Week 2 exercise used:

```sql
PARTITION BY RANGE (pickup_datetime)
```

Range partitioning divides records according to value ranges.

For example:

```text
December:
2025-12-01 → 2026-01-01

January:
2026-01-01 → 2026-02-01
```

---

# Checking the Data Before Designing Partitions

Before creating partitions, the actual date range was checked:

```sql
SELECT MIN(pickup_datetime) AS earliest_pickup,
       MAX(pickup_datetime) AS latest_pickup
FROM taxi_trips;
```

The result was:

```text
Earliest:
2025-12-31 23:57:29

Latest:
2026-01-07 17:08:32
```

This was an important data-engineering lesson.

Even though the source file represented January 2026 Yellow Taxi data, the sample contained pickup timestamps from December 2025.

Therefore, the partition design was based on the **actual data**, not just the source filename.

---

# Creating the Parent Table

A new partitioned table was created:

```sql
CREATE TABLE taxi_trips_partitioned
(
    LIKE taxi_trips INCLUDING ALL
)
PARTITION BY RANGE (pickup_datetime);
```

`LIKE taxi_trips INCLUDING ALL` copied the table structure.

It did **not** copy the 500,000 records.

Therefore the new parent initially contained:

```text
0 rows
```

---

# Creating Child Partitions

Two child partitions were required.

## December 2025

```sql
CREATE TABLE taxi_trips_2025_12
PARTITION OF taxi_trips_partitioned
FOR VALUES FROM ('2025-12-01')
TO ('2026-01-01');
```

## January 2026

```sql
CREATE TABLE taxi_trips_2026_01
PARTITION OF taxi_trips_partitioned
FOR VALUES FROM ('2026-01-01')
TO ('2026-02-01');
```

---

# Partition Boundaries

An important concept learned during this exercise was:

```text
FROM → inclusive
TO   → exclusive
```

Therefore:

```sql
FROM ('2026-01-01')
TO ('2026-02-01')
```

means:

```text
pickup_datetime >= 2026-01-01
AND
pickup_datetime < 2026-02-01
```

This represents the full month of January.

Using the first day of the following month also avoids needing to manually reason about whether a month has 28, 29, 30 or 31 days.

---

# Non-Overlapping Partitions

Range partitions must not overlap.

Correct:

```text
December:
Dec 1 → Jan 1

January:
Jan 1 → Feb 1
```

Incorrect:

```text
December:
Dec 1 → Jan 1

January:
Dec 31 → Feb 1
```

The incorrect version overlaps with the December range.

---

# Loading Data Through the Parent

The existing taxi records were inserted into the partitioned parent:

```sql
INSERT INTO taxi_trips_partitioned
SELECT *
FROM taxi_trips;
```

The rows did not need to be manually inserted into each child table.

PostgreSQL examined the partition key:

```text
pickup_datetime
```

and automatically routed each record into the correct partition.

---

# Actual Partition Results

After loading the 500,000-row sample:

```text
taxi_trips_partitioned
│
├── taxi_trips_2025_12 →       6 rows
│
└── taxi_trips_2026_01 → 499,994 rows
```

Total:

```text
500,000 rows
```

This confirmed that six records from the January source sample had December pickup timestamps.

---

# Partition Pruning

Partition pruning means PostgreSQL can exclude partitions that cannot contain records required by the query.

The Week 2 test was:

```sql
EXPLAIN
SELECT *
FROM taxi_trips_partitioned
WHERE pickup_datetime >= '2025-12-01'
  AND pickup_datetime < '2026-01-01';
```

The execution plan contained:

```text
Seq Scan on taxi_trips_2025_12
```

The January partition did not appear in the plan.

PostgreSQL recognized that:

```text
taxi_trips_2026_01
```

could not contain records matching the December condition.

It therefore pruned the January partition.

---

# Partition Pruning vs Sequential Scan

These concepts describe different parts of query execution.

## Partition Pruning

Answers:

> Which partitions need to be searched?

## Sequential / Index Scan

Answers:

> How should PostgreSQL search inside the selected table or partition?

Therefore:

```text
Partition pruning
+
Sequential scan
```

is completely valid.

In the December example, PostgreSQL correctly selected only the December partition and then sequentially scanned that very small partition.

---

# Partitioning Strategy

Partitions should be designed according to actual data and query patterns.

For example, if analysts commonly ask:

```text
Show trips from February 2026
```

then time-based partitioning can be useful.

A possible large-scale design is:

```text
Taxi trips
│
├── 2026-01
├── 2026-02
├── 2026-03
├── ...
├── 2027-01
└── ...
```

---

# What Is Clustering?

Clustering generally refers to organizing related values physically closer together so queries filtering those values can access data more efficiently.

Suppose taxi analytics commonly follows this pattern:

```text
1. Filter by month
2. Filter/group by pickup location
```

A conceptual warehouse design could be:

```text
Partition:
pickup_datetime

Cluster / organize:
pu_location_id
```

Partitioning first eliminates irrelevant time periods.

Clustering can then help organize records within the relevant data around pickup locations.

---

# PostgreSQL CLUSTER vs Warehouse Clustering

PostgreSQL provides a `CLUSTER` command, but it should not be confused with clustering implementations in cloud analytical warehouses.

PostgreSQL can physically reorder a table according to an existing index.

Conceptually:

```sql
CLUSTER taxi_trips
USING idx_taxi_pu_location;
```

However, PostgreSQL does not continuously maintain that physical ordering as new records are inserted or updated.

Cloud data warehouses such as BigQuery and Snowflake use different storage and clustering mechanisms.

Therefore, the broader Week 2 concept was to understand **why data may be organized around frequently filtered columns**, rather than assuming all database systems implement clustering identically.

---

# Partitioning vs Clustering

## Partitioning

```text
Divide a dataset into separate sections.
```

Example:

```text
January
February
March
```

## Clustering

```text
Organize related values within the stored data.
```

Example:

```text
pickup location
```

A useful conceptual design for a large taxi warehouse could therefore be:

```text
Partition by time
+
Cluster/organize by location
```

when that matches the actual query workload.

---

# Important Design Principle

Database physical design should follow **real query patterns**.

A column should not be chosen as a partition or clustering key simply because it exists.

Instead, consider:

```text
What columns are frequently filtered?
What time ranges are queried?
How much data is scanned?
How selective are the filters?
How is the data loaded?
How large will the dataset become?
```

---

# Key Takeaways

- Partitioning divides a large logical table into smaller physical sections.
- Range partitioning is useful for time-based datasets.
- The partition key used in Week 2 was `pickup_datetime`.
- Actual source data should be inspected before designing partitions.
- `FROM` is inclusive and `TO` is exclusive.
- Monthly partitions can use the first day of consecutive months as boundaries.
- PostgreSQL automatically routes inserted rows to the appropriate partition.
- The 500,000-row sample produced 6 December records and 499,994 January records.
- Partition pruning allows PostgreSQL to skip irrelevant partitions.
- Partition pruning and scan type are different concepts.
- Clustering and partitioning solve different physical-organization problems.
- PostgreSQL `CLUSTER` differs from cloud warehouse clustering.
- Partition and clustering keys should reflect real query patterns.