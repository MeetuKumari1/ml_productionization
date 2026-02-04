import json
import os
from pathlib import Path

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


def _load_flight_model():
    if not FLIGHT_MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {FLIGHT_MODEL_PATH}. "
            "Run src/training/train_model.py to create it."
        )
    return joblib.load(FLIGHT_MODEL_PATH)


def _load_flight_metadata():
    if FLIGHT_METADATA_PATH.exists():
        return json.loads(FLIGHT_METADATA_PATH.read_text(encoding="utf-8"))
    return {}


def _load_gender_model():
    if not GENDER_MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {GENDER_MODEL_PATH}. "
            "Run src/training/train_gender_model.py to create it."
        )
    return joblib.load(GENDER_MODEL_PATH)


def _load_gender_metadata():
    if GENDER_METADATA_PATH.exists():
        return json.loads(GENDER_METADATA_PATH.read_text(encoding="utf-8"))
    return {}


def _validate_flight_payload(payload):
    if isinstance(payload, dict) and "instances" in payload:
        instances = payload.get("instances")
    else:
        instances = [payload]

    if not isinstance(instances, list) or not instances:
        raise ValueError("Payload must be an object or a non-empty instances list.")

    cleaned = []
    for idx, item in enumerate(instances):
        if not isinstance(item, dict):
            raise ValueError(f"Instance at index {idx} must be an object.")
        missing = [c for c in FLIGHT_FEATURE_COLUMNS if c not in item]
        if missing:
            raise ValueError(f"Missing fields in instance {idx}: {missing}")
        cleaned.append(item)

    df = pd.DataFrame(cleaned, columns=FLIGHT_FEATURE_COLUMNS)
    df["time"] = pd.to_numeric(df["time"], errors="raise")
    df["distance"] = pd.to_numeric(df["distance"], errors="raise")
    return df


def _validate_gender_payload(payload):
    if isinstance(payload, dict) and "instances" in payload:
        instances = payload.get("instances")
    else:
        instances = [payload]

    if not isinstance(instances, list) or not instances:
        raise ValueError("Payload must be an object or a non-empty instances list.")

    cleaned = []
    for idx, item in enumerate(instances):
        if not isinstance(item, dict):
            raise ValueError(f"Instance at index {idx} must be an object.")
        missing = [c for c in GENDER_FEATURE_COLUMNS if c not in item]
        if missing:
            raise ValueError(f"Missing fields in instance {idx}: {missing}")
        cleaned.append(item)

    df = pd.DataFrame(cleaned, columns=GENDER_FEATURE_COLUMNS)
    df["age"] = pd.to_numeric(df["age"], errors="raise")
    return df


@app.get("/health")
def health():
    metadata = _load_flight_metadata()
    gender_meta = _load_gender_metadata()
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
        df = _validate_flight_payload(payload)
        model = _load_flight_model()
        preds = model.predict(df).tolist()
        return jsonify({"predictions": preds})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


@app.post("/predict_gender")
def predict_gender():
    try:
        payload = request.get_json(force=True)
        df = _validate_gender_payload(payload)
        model = _load_gender_model()
        preds = model.predict(df).tolist()
        return jsonify({"predictions": preds})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
