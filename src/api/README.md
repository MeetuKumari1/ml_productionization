# Prediction API

This Flask API serves two models:

- Flight price regression
- User gender classification

## Endpoints

### Health

`GET /health`

Returns model metadata and load status.

### Flight Price Prediction

`POST /predict`

Payload format:

```
{"instances":[{"from":"MAD","to":"NYC","flightType":"First","agency":"TravelCo","time":9.5,"distance":4600}]}
```

Response:

```
{"predictions":[1234.56]}
```

### Gender Prediction

`POST /predict_gender`

Payload format:

```
{"instances":[{"company":"Acme","name":"Taylor", "age":29}]}
```

Response:

```
{"predictions":["F"]}
```

## Running Locally

1. Train or provide the models:
   - `python src/training/train_model.py`
   - `python src/training/train_gender_model.py`
2. Start the API:
   - `python src/api/app.py`

## Environment Variables

- `PORT` (default: 5000)

## Artifacts

The API expects:

- `artifacts/flight_price_model.joblib`
- `artifacts/user_gender_model.joblib`
- Optional metadata: `artifacts/metadata.json`, `artifacts/user_gender_metadata.json`
