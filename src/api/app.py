"""Flask API for flight price and gender prediction models."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from flask import Flask, jsonify, request

FLIGHT_MODEL_PATH = Path("artifacts/flight_price_model.joblib")
FLIGHT_METADATA_PATH = Path("artifacts/metadata.json")
GENDER_MODEL_PATH = Path("artifacts/user_gender_model.joblib")
GENDER_METADATA_PATH = Path("artifacts/user_gender_metadata.json")

FLIGHT_FEATURE_COLUMNS = ["from", "to", "flightType", "agency", "time", "distance"]
GENDER_FEATURE_COLUMNS = ["company", "name", "age"]

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify(
        {
            "message": "ML Productionization API",
            "endpoints": {
                "health": "/health",
                "predict_flight_price": "/predict",
                "predict_gender": "/predict_gender",
            },
        }
    )


def _load_model(model_path: Path, hint: str) -> Any:
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found at {model_path}. {hint}")
    return joblib.load(model_path)


def _load_metadata(metadata_path: Path) -> dict:
    if not metadata_path.exists():
        return {}
    return json.loads(metadata_path.read_text(encoding="utf-8"))


def _normalize_instances(payload: Any) -> list[dict]:
    if isinstance(payload, dict) and "instances" in payload:
        instances = payload.get("instances")
    else:
        instances = [payload]

    if not isinstance(instances, list) or not instances:
        raise ValueError("Payload must be an object or a non-empty instances list.")

    cleaned: list[dict] = []
    for idx, item in enumerate(instances):
        if not isinstance(item, dict):
            raise ValueError(f"Instance at index {idx} must be an object.")
        cleaned.append(item)
    return cleaned


def _validate_payload(
    *,
    payload: Any,
    required_columns: list[str],
    numeric_columns: list[str],
) -> pd.DataFrame:
    instances = _normalize_instances(payload)

    for idx, item in enumerate(instances):
        missing = [column for column in required_columns if column not in item]
        if missing:
            raise ValueError(f"Missing fields in instance {idx}: {missing}")

    df = pd.DataFrame(instances, columns=required_columns)
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="raise")
    return df


@app.get("/health")
def health():
    metadata = _load_metadata(FLIGHT_METADATA_PATH)
    gender_meta = _load_metadata(GENDER_METADATA_PATH)
    return jsonify(
        {
            "status": "ok",
            "model_loaded": FLIGHT_MODEL_PATH.exists(),
            "model_name": metadata.get("model_name"),
            "features": metadata.get("features", FLIGHT_FEATURE_COLUMNS),
            "gender_model_loaded": GENDER_MODEL_PATH.exists(),
            "gender_model_name": gender_meta.get("model_name"),
            "gender_features": gender_meta.get("features", GENDER_FEATURE_COLUMNS),
        }
    )


@app.post("/predict")
def predict():
    try:
        payload = request.get_json(force=True)
        df = _validate_payload(
            payload=payload,
            required_columns=FLIGHT_FEATURE_COLUMNS,
            numeric_columns=["time", "distance"],
        )
        model = _load_model(
            FLIGHT_MODEL_PATH,
            "Run src/training/train_model.py to create it.",
        )
        preds = model.predict(df).tolist()
        return jsonify({"predictions": preds})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


@app.post("/predict_gender")
def predict_gender():
    try:
        payload = request.get_json(force=True)
        df = _validate_payload(
            payload=payload,
            required_columns=GENDER_FEATURE_COLUMNS,
            numeric_columns=["age"],
        )
        model = _load_model(
            GENDER_MODEL_PATH,
            "Run src/training/train_gender_model.py to create it.",
        )
        preds = model.predict(df).tolist()
        return jsonify({"predictions": preds})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
