import json
import os
from pathlib import Path

import joblib
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

DATA_PATH = Path("travel_capstone/flights.csv")
MODEL_PATH = Path("artifacts/flight_price_model.joblib")
METADATA_PATH = Path("artifacts/metadata.json")

FEATURE_COLUMNS = ["from", "to", "flightType", "agency", "time", "distance"]
TARGET_COLUMN = "price"


def _load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. "
            "Set DATA_PATH or place flights.csv under travel_capstone/."
        )
    df = pd.read_csv(DATA_PATH)
    return df


def _build_preprocess():
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), ["time", "distance"]),
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["from", "to", "flightType", "agency"]),
        ]
    )


def _rmse(y_true, y_pred):
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def main():
    tracking_uri = os.environ.get("MLFLOW_TRACKING_URI")
    if not tracking_uri:
        db_path = Path("mlflow.db").resolve()
        tracking_uri = f"sqlite:///{db_path.as_posix()}"
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(os.environ.get("MLFLOW_EXPERIMENT", "flight-price-regression"))

    df = _load_data()
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    preprocess = _build_preprocess()

    models = {
        "LinearRegression": LinearRegression(),
        "Ridge": Ridge(alpha=1.0),
        "Lasso": Lasso(alpha=0.01, max_iter=10000, tol=1e-4),
        "RandomForest": RandomForestRegressor(
            n_estimators=300, max_depth=None, random_state=42, n_jobs=-1
        ),
        "GradientBoosting": GradientBoostingRegressor(
            n_estimators=300, learning_rate=0.05, max_depth=3, random_state=42
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
            mlflow.log_param("test_size", 0.2)
            mlflow.log_metric("rmse", rmse)

    best_model_name = min(scores, key=scores.get)
    best_model = models[best_model_name]

    best_pipeline = Pipeline(steps=[("preprocess", preprocess), ("model", best_model)])
    best_pipeline.fit(X, y)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_pipeline, MODEL_PATH)

    metadata = {
        "model_name": best_model_name,
        "rmse": scores[best_model_name],
        "features": FEATURE_COLUMNS,
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    with mlflow.start_run(run_name="best_model") as run:
        mlflow.log_param("model_name", best_model_name)
        mlflow.log_metric("rmse", scores[best_model_name])
        mlflow.sklearn.log_model(best_pipeline, artifact_path="model")
        mlflow.log_artifact(str(METADATA_PATH))

    print(f"Saved model to {MODEL_PATH}")
    print(f"Best model: {best_model_name} (RMSE={scores[best_model_name]:.4f})")


if __name__ == "__main__":
    main()
