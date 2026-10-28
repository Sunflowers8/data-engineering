# Week 8 — Docker & CI/CD

## Overview

Built a containerized Python taxi revenue application and
an automated CI workflow using GitHub Actions.

The project demonstrates Docker image creation, versioning,
Docker Compose, automated unit testing, and CI validation.

## Technologies

- Python 3.12
- Docker and Docker Compose
- Python unittest
- GitHub Actions

## Application

The taxi application processes four sample taxi trips and
calculates their total revenue using Python Decimal.

Expected result:

- Total trips: 4
- Total revenue: $60.50

## Project Structure

    08-week-docker-cicd/
    ├── README.md
    └── taxi-app/
        ├── app.py
        ├── test_app.py
        ├── Dockerfile
        ├── compose.yaml
        └── .dockerignore

The CI workflow is located at:

    .github/workflows/week8-taxi-ci.yml

## Run Locally

From the repository root:

    cd 08-week-docker-cicd/taxi-app
    python app.py

## Run Unit Tests

    python -m unittest -v test_app

Three tests cover:

1. Correct revenue for four taxi trips
2. Empty input
3. Decimal precision

## Build and Run Docker

    docker build -t taxi-revenue:local .
    docker run --rm taxi-revenue:local

Run automated tests inside Docker:

    docker run --rm taxi-revenue:local python -m unittest -v test_app

## Docker Compose

Validate configuration:

    docker compose config --quiet

Run the taxi application:

    docker compose run --rm taxi-app

## GitHub Actions CI

The Week 8 workflow is configured to run when relevant
application or workflow files change, on applicable pull
requests, or when manually triggered.

The workflow performs:

1. Repository checkout
2. Python 3.12 setup
3. Python unit testing
4. Local application execution
5. Docker image build
6. Unit testing inside Docker
7. Application execution inside Docker

## Key Learning Outcomes

- Understand the difference between images and containers
- Create and build Dockerfiles
- Use versioned Docker images
- Understand Docker layer caching
- Configure Docker Compose
- Write automated Python unit tests
- Execute tests inside containers
- Configure GitHub Actions workflows

## Status

Local Python tests and Docker tests passed.

GitHub Actions execution will be verified after publishing
the workflow to GitHub.
