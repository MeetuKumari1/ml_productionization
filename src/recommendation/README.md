# Recommendation System

The recommender is an item-item similarity model trained on user hotel bookings.

## Data Requirements

- `travel_capstone/hotels.csv`
- `travel_capstone/users.csv` (used by the Streamlit app)

## Train the Recommender

Run the CLI entrypoint:

- `python src/recommendation/train_hotel_recommender.py`

Artifacts created:

- `artifacts/hotel_recommender.joblib`
- `artifacts/hotel_recommender_metadata.json`

## Using the Recommender

The main functions live in `recommender.py`:

- `train_recommender()` to build and save artifacts
- `load_recommender()` to load the model
- `recommend_for_user()` to fetch recommendations
