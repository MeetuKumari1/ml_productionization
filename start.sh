#!/bin/sh
set -e

if [ ! -f artifacts/flight_price_model.joblib ]; then
  if [ -f travel_capstone/flights.csv ]; then
    python src/training/train_model.py
  else
    echo "Model not found and dataset missing at travel_capstone/flights.csv" >&2
    exit 1
  fi
fi

if [ ! -f artifacts/user_gender_model.joblib ]; then
  if [ -f travel_capstone/users.csv ]; then
    python src/training/train_gender_model.py
  else
    echo "Gender model not found and dataset missing at travel_capstone/users.csv" >&2
    exit 1
  fi
fi

exec python src/api/app.py
