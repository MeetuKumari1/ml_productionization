import json
import os
from pathlib import Path

import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

FEATURE_COLUMNS = ["from", "to", "flightType", "agency", "time", "distance"]
TARGET_COLUMN = "price"
CAT_COLS = ["from", "to", "flightType", "agency"]
NUM_COLS = ["time", "distance"]


def load_data(data_path: str) -> pd.DataFrame:
    path = Path(data_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    return pd.read_csv(path)


def validate_data(df: pd.DataFrame) -> None:
    missing_cols = [c for c in FEATURE_COLUMNS + [TARGET_COLUMN] if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")

    if df[FEATURE_COLUMNS + [TARGET_COLUMN]].isna().any().any():
        raise ValueError("Dataset contains missing values in required columns.")

    if not np.issubdtype(df["time"].dtype, np.number):
        raise ValueError("time column must be numeric.")
    if not np.issubdtype(df["distance"].dtype, np.number):
        raise ValueError("distance column must be numeric.")


def _build_preprocess() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUM_COLS),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CAT_COLS),
        ]
    )


def _rmse(y_true, y_pred) -> float:
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def train_and_select_model(
    data_path: str,
    artifacts_dir: str,
    test_size: float = 0.2,
    random_state: int = 42,
) -> dict:
    tracking_uri = os.environ.get("MLFLOW_TRACKING_URI")
    if not tracking_uri:
        db_path = Path("mlflow.db").resolve()
        tracking_uri = f"sqlite:///{db_path.as_posix()}"
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(os.environ.get("MLFLOW_EXPERIMENT", "flight-price-regression"))

    df = load_data(data_path)
    validate_data(df)

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    preprocess = _build_preprocess()

    models = {
        "LinearRegression": LinearRegression(),
        "Ridge": Ridge(alpha=1.0),
        "Lasso": Lasso(alpha=0.01),
        "RandomForest": RandomForestRegressor(
            n_estimators=300, max_depth=None, random_state=random_state, n_jobs=-1
        ),
        "GradientBoosting": GradientBoostingRegressor(
            n_estimators=300, learning_rate=0.05, max_depth=3, random_state=random_state
        ),
    }

    scores = {}
    for name, model in models.items():
        pipe = Pipeline(steps=[("preprocess", preprocess), ("model", model)])
        with mlflow.start_run(run_name=name):
            pipe.fit(X_train, y_train)
            preds = pipe.predict(X_val)
            rmse = _rmse(y_val, preds)
            scores[name] = rmse

            mlflow.log_param("model_name", name)
            mlflow.log_param("test_size", test_size)
            mlflow.log_metric("rmse", rmse)

    best_model_name = min(scores, key=scores.get)
    best_model = models[best_model_name]

    best_pipeline = Pipeline(steps=[("preprocess", preprocess), ("model", best_model)])
    best_pipeline.fit(X, y)

    artifacts_path = Path(artifacts_dir)
    artifacts_path.mkdir(parents=True, exist_ok=True)

    model_path = artifacts_path / "flight_price_model.joblib"
    metadata_path = artifacts_path / "metadata.json"

    import joblib

    joblib.dump(best_pipeline, model_path)
    metadata = {
        "model_name": best_model_name,
        "rmse": scores[best_model_name],
        "features": FEATURE_COLUMNS,
        "data_path": str(Path(data_path).resolve()),
    }
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    with mlflow.start_run(run_name="best_model"):
        mlflow.log_param("model_name", best_model_name)
        mlflow.log_metric("rmse", scores[best_model_name])
        mlflow.sklearn.log_model(best_pipeline, artifact_path="model")
        mlflow.log_artifact(str(metadata_path))

    return metadata
