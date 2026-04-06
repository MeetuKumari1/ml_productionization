# Airflow Pipeline

This directory contains the Airflow DAG that validates data and trains the flight price model on a schedule.

## DAG

- `flight_price_pipeline_dag.py`
- DAG id: `flight_price_training_pipeline`
- Schedule: `@daily`

## Configuration

Set these environment variables in the Airflow environment:

- `FLIGHT_DATA_PATH` (default: `/opt/airflow/data/travel_capstone/flights.csv`)
- `FLIGHT_ARTIFACTS_DIR` (default: `/opt/airflow/artifacts`)

## Notes

The DAG imports `src/pipeline/flight_workflow.py`, so the `src/` path must be available on the Airflow worker. The DAG file appends it to `sys.path` at runtime.
