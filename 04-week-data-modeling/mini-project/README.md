# Week 4 Mini-Project — NYC Taxi Dimensional Warehouse

## Project Overview

This project converts NYC Yellow Taxi trip data into a dimensional warehouse model in PostgreSQL.

The objective was to move beyond storing raw taxi records and design an analytics-friendly star schema using fact and dimension tables.

## Dataset

NYC Yellow Taxi trip data was used as the primary dataset.

A 500,000-row sample was loaded into PostgreSQL for practical warehouse modeling.

An official NYC Taxi Zone lookup dataset was also used to create the location dimension.

## Architecture

```text
NYC Taxi Trip Data
        |
        v
  Source taxi_trips
        |
        v
Dimension Lookups
        |
        v
+-----------------------+
|    fact_taxi_trip     |
+-----------------------+
   /      |      |    \
  v       v      v     v
Date   Location Vendor Payment
```

`dim_location` is used twice:

```text
Pickup location
Dropoff location
```

## Grain

The grain of `fact_taxi_trip` is:

> One row represents one NYC taxi trip.

## Dimensions

The warehouse contains:

```text
dim_date
dim_location
dim_vendor
dim_payment_type
```

## Fact Table

The central fact table is:

```text
fact_taxi_trip
```

Dimension foreign keys:

```text
pickup_date_key
pickup_location_key
dropoff_location_key
payment_type_key
vendor_key
```

Measures:

```text
passenger_count
trip_distance
fare_amount
tip_amount
tolls_amount
total_amount
trip_duration_minutes
```

## Location Dimension

The NYC Taxi Zone lookup file contained:

```text
265 rows
4 source columns
```

Source columns included:

```text
LocationID
Borough
Zone
service_zone
```

The data was transformed into:

```text
location_id
borough
zone
service_zone
```

Missing descriptive values were filled with:

```text
Unknown
```

The resulting 265 records were loaded into `dim_location`.

## Vendor Dimension

The vendor dimension was populated with known vendor identifiers and names.

Example structure:

```text
vendor_key
vendor_id
vendor_name
```

`vendor_key` is the warehouse surrogate key.

`vendor_id` is the source/business key.

## Payment Type Dimension

The payment dimension initially contained source IDs 1–6.

During fact-load validation, the source dataset was found to also contain:

```text
payment_type = 0
```

This represents:

```text
Flex Fare
```

Because an INNER JOIN would have removed these trips, payment type 0 was added to the dimension.

Final payment-type dimension size:

```text
7 records
```

## Date Dimension

`dim_date` contains:

```text
date_key
full_date
day
day_name
month
month_name
quarter
year
is_weekend
```

Date keys follow:

```text
YYYYMMDD
```

Example:

```text
2026-10-06 → 20261006
```

January 2026 was generated using PostgreSQL `generate_series()`.

Initial January records:

```text
31
```

## Data Quality Discovery

Before loading the fact table, the source records were compared with the date dimension.

Initial check:

```text
total trips     = 500000
matched dates   = 499994
unmatched dates = 6
```

Investigation identified:

```text
missing date = 2025-12-31
trip count   = 6
```

Instead of silently dropping these records, the valid date was added to `dim_date`.

Final validation:

```text
unmatched_dates = 0
```

## Dimension Lookup Strategy

The source contains business identifiers.

Example:

```text
taxi_trips.vendor_id
```

The warehouse fact table requires the surrogate key.

Lookup:

```sql
JOIN dim_vendor v
    ON t.vendor_id = v.vendor_id
```

Then:

```text
v.vendor_key
```

is stored in the fact table.

The same approach is used for:

```text
location
payment type
date
```

## Role-Playing Location Dimension

The same location dimension represents two different roles.

```sql
JOIN dim_location pickup
    ON t.pu_location_id = pickup.location_id

JOIN dim_location dropoff
    ON t.do_location_id = dropoff.location_id
```

This avoids creating separate physical pickup and dropoff dimension tables.

## Fact Load

After validating dimension coverage, the fact table was populated using dimension joins.

Conceptually:

```text
taxi_trips
    |
    +--> dim_date
    +--> dim_location (pickup)
    +--> dim_location (dropoff)
    +--> dim_vendor
    +--> dim_payment_type
    |
    v
fact_taxi_trip
```

The project used a 500,000-row taxi sample for the warehouse implementation.

## Data Engineering Lessons

This project demonstrated:

- Defining fact-table grain
- Separating facts and dimensions
- Business vs surrogate keys
- Primary and foreign keys
- Star-schema design
- Role-playing dimensions
- Date dimensions
- Dimension lookups
- Data-quality validation
- Missing-dimension handling
- Avoiding silent row loss
- Loading an analytical fact table

## Important Lesson

A successful SQL query does not automatically mean the data model is correct.

Before loading facts, source row counts and dimension matches should be validated.

This project discovered real unmatched records before the final load and corrected the dimensions rather than silently discarding source data.

## Technologies

```text
Python
Pandas
PostgreSQL
SQLAlchemy
DBeaver
Git
GitHub
```

## Related Files

```text
../ddl/create_star_schema.sql
../dimensional-model/star_schema.md
../dimensional-model/inspect_taxi_zones.py
../dimensional-model/load_location_dimension.py
../dimensional-model/load_date_dimension.py
../erd/nyc-taxi-star-schema.md
```
