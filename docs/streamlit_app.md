# Streamlit App

The Streamlit app provides hotel recommendations and data insights.

## Run Locally

1. Install dependencies:
   - `pip install -r requirements.txt`
2. Start the app:
   - `streamlit run streamlit_app.py`

## Data Requirements

Ensure the following data files are available:

- `travel_capstone/hotels.csv`
- `travel_capstone/users.csv`

## Model Behavior

The app loads `artifacts/hotel_recommender.joblib` if present. If the model is missing, use the **Train Recommender** button to generate it.
