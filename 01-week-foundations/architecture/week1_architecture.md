# Week 01 — Data Pipeline Architecture

## Overview

This architecture represents the practical data pipeline developed during Week 1 of my Data Engineering internship learning.

The pipeline demonstrates a basic ETL workflow using CSV files, Python, Pandas, PostgreSQL and SQL.

## Architecture

```text
┌─────────────────────┐
│    Raw CSV Data     │
│   employees.csv     │
└──────────┬──────────┘
           │
           │ Extract
           ▼
┌─────────────────────┐
│   Python / Pandas   │
│                     │
│ Cleaning            │
│ Missing Values      │
│ Filtering           │
│ Transformations     │
└──────────┬──────────┘
           │
           │ Transform
           ▼
┌─────────────────────┐
│    Processed CSV    │
│ employees_cleaned   │
└──────────┬──────────┘
           │
           │ Load
           ▼
┌─────────────────────┐
│    PostgreSQL 16    │
│                     │
│ DB: employee_db     │
│ Table: employee     │
└──────────┬──────────┘
           │
           │ SQL Queries
           ▼
┌─────────────────────┐
│      DBeaver        │
│                     │
│ Querying            │
│ Analysis            │
│ Results             │
└─────────────────────┘