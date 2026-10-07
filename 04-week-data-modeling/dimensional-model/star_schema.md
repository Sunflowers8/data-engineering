# NYC Taxi Star Schema

## Fact Table Grain

**fact_taxi_trip**

Grain: One row represents one NYC taxi trip.

## Dimension Tables

### dim_payment_type

| Column | Description |
|---|---|
| payment_type_key | Surrogate key |
| payment_type_id | Source/business key |
| payment_type_name | Description of payment method |


### dim_location

| Column | Description |
|---|---|
| location_key | Surrogate key |
| location_id | Source/business key |
| borough | Borough name |
| zone | Taxi zone name |
| service_zone | Service zone |

### dim_vendor

| Column | Description |
|---|---|
| vendor_id | Source/business key |
| vendor_key | Surrogate key |
| vendor_name | vendor descriptin or name |

### dim_date

| Column | Description |
|---|---|
| date_key | Surrogate key |
| full_date | Source/business date |
| day | Day of the month |
| day_name | Name of the day of the week |
| month | Month number |
| month_name | Name of the month |
| quarter | Quarter of the year |
| year | Calendar year |
| is_weekend | Indicates whether the date falls on a weekend |