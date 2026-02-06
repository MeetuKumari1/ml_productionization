import json
import os
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

DATA_PATH = Path("travel_capstone/users.csv")
MODEL_PATH = Path("artifacts/user_gender_model.joblib")
METADATA_PATH = Path("artifacts/user_gender_metadata.json")

FEATURE_COLUMNS = ["company", "name", "age"]
TARGET_COLUMN = "gender"


def _load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. "
            "Set DATA_PATH or place users.csv under travel_capstone/."
        )
    return pd.read_csv(DATA_PATH)


def _build_preprocess():
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), ["age"]),
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["company"]),
            ("name", TfidfVectorizer(ngram_range=(1, 2)), "name"),
        ]
    )


def main():
    tracking_uri = os.environ.get("MLFLOW_TRACKING_URI")
    if not tracking_uri:
        db_path = Path("mlflow.db").resolve()
        tracking_uri = f"sqlite:///{db_path.as_posix()}"
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(os.environ.get("MLFLOW_EXPERIMENT", "user-gender-classification"))

    df = _load_data()
    if df[FEATURE_COLUMNS + [TARGET_COLUMN]].isna().any().any():
        raise ValueError("Dataset contains missing values in required columns.")

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    preprocess = _build_preprocess()
    model = LogisticRegression(max_iter=1000)

    pipeline = Pipeline(steps=[("preprocess", preprocess), ("model", model)])

    with mlflow.start_run(run_name="logreg_gender"):
        pipeline.fit(X_train, y_train)
        preds = pipeline.predict(X_val)
        acc = float(accuracy_score(y_val, preds))

        mlflow.log_param("model_name", "LogisticRegression")
        mlflow.log_param("max_iter", 1000)
        mlflow.log_metric("accuracy", acc)

        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(pipeline, MODEL_PATH)

        metadata = {
            "model_name": "LogisticRegression",
            "accuracy": acc,
            "features": FEATURE_COLUMNS,
        }
        METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

        mlflow.sklearn.log_model(pipeline, artifact_path="model")
        mlflow.log_artifact(str(METADATA_PATH))

    print(f"Saved model to {MODEL_PATH}")
    print(f"Validation accuracy: {acc:.4f}")


if __name__ == "__main__":
    main()
