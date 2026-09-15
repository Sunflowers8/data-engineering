# Week 1 Data Pipeline Architecture

Employee CSV Source
        |
        v
Python / Pandas
Extract, Clean & Transform
        |
        v
Cleaned CSV
        |
        v
PostgreSQL 16
employee_db
        |
        v
employee table
        |
        v
SQL Analytics / Serving