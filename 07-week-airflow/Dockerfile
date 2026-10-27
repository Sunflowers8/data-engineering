FROM apache/airflow:3.1.7

USER airflow

COPY --chown=airflow:0 07-week-airflow/requirements-dbt.txt /tmp/requirements-dbt.txt

RUN python -m venv /opt/airflow/taxi-venv \
    && /opt/airflow/taxi-venv/bin/pip install --no-cache-dir \
       -r /tmp/requirements-dbt.txt

COPY --chown=airflow:0 06-week-dbt/nyc_taxi_dbt /opt/airflow/nyc_taxi_dbt

RUN chmod -R g=u /opt/airflow/nyc_taxi_dbt
