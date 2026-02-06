# Model Training

This folder contains the training scripts for the flight price regression model and the user gender classification model.

## Flight Price Regression

Script: `src/training/train_model.py`

Input:

- `travel_capstone/flights.csv`

Output:

- `artifacts/flight_price_model.joblib`
- `artifacts/metadata.json`

Run:

- `python src/training/train_model.py`

## Gender Classification

Script: `src/training/train_gender_model.py`

Input:

- `travel_capstone/users.csv`

Output:

- `artifacts/user_gender_model.joblib`
- `artifacts/user_gender_metadata.json`

Run:

- `python src/training/train_gender_model.py`

## MLflow Tracking

Both scripts log runs to MLflow. Configure with:

- `MLFLOW_TRACKING_URI`
- `MLFLOW_EXPERIMENT`
