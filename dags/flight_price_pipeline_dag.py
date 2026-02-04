from datetime import datetime
from pathlib import Path
import os
import sys

from airflow import DAG
from airflow.operators.python import PythonOperator

BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from src.pipeline.flight_workflow import load_data, train_and_select_model, validate_data

DATA_PATH = os.environ.get(
    "FLIGHT_DATA_PATH",
    "/opt/airflow/data/travel_capstone/flights.csv",
)
ARTIFACTS_DIR = os.environ.get("FLIGHT_ARTIFACTS_DIR", "/opt/airflow/artifacts")


def _validate():
    df = load_data(DATA_PATH)
    validate_data(df)


def _train():
    train_and_select_model(DATA_PATH, ARTIFACTS_DIR)


default_args = {
    "owner": "mlops",
    "retries": 1,
}

with DAG(
    dag_id="flight_price_training_pipeline",
    default_args=default_args,
    description="Train and select best regression model for flight price prediction.",
    schedule="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["ml", "regression", "flight"],
) as dag:
    validate_task = PythonOperator(
        task_id="validate_data",
        python_callable=_validate,
    )

    train_task = PythonOperator(
        task_id="train_and_select_model",
        python_callable=_train,
    )

    validate_task >> train_task
