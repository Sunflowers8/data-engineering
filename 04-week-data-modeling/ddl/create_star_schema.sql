CREATE TABLE dim_payment_type (
    payment_type_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    payment_type_id INTEGER,
    payment_type_name VARCHAR(50)
);

CREATE TABLE dim_vendor (
    vendor_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    vendor_id INTEGER,
    vendor_name VARCHAR(100)
);

CREATE TABLE dim_location (
    location_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    location_id INTEGER,
    borough VARCHAR(50),
    zone VARCHAR(50),
    service_zone VARCHAR(50)
);

CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE,
    day INTEGER,
    day_name VARCHAR(10),
    month INTEGER,
    month_name VARCHAR (10),
    quarter INTEGER,
    year INTEGER,
    is_weekend BOOLEAN
);

CREATE TABLE fact_taxi_trip (
    pickup_date_key INTEGER REFERENCES dim_date(date_key),
    pickup_location_key INTEGER REFERENCES dim_location(location_key),
    dropoff_location_key INTEGER REFERENCES dim_location(location_key),
    payment_type_key INTEGER REFERENCES dim_payment_type(payment_type_key) ,
    vendor_key INTEGER REFERENCES dim_vendor(vendor_key) ,
    trip_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    passenger_count INTEGER,
    trip_distance NUMERIC,
    fare_amount NUMERIC,
    tip_amount NUMERIC,
    tolls_amount NUMERIC,
    total_amount NUMERIC,
    trip_duration_minutes NUMERIC
);