import pandas as pd
import streamlit as st

from src.recommendation.recommender import (
    HOTELS_PATH,
    USERS_PATH,
    load_hotels,
    load_recommender,
    train_recommender,
    recommend_for_user,
)

st.set_page_config(page_title="Travel Hotel Recommendations", layout="wide")


@st.cache_data
def _load_users():
    return pd.read_csv(USERS_PATH)


@st.cache_data
def _load_hotels():
    return load_hotels(HOTELS_PATH)


@st.cache_resource
def _load_model():
    return load_recommender()


st.title("Hotel Recommendations & Insights")

left, right = st.columns([1, 2])

with left:
    st.subheader("Model")
    if st.button("Train Recommender"):
        train_recommender()
        st.success("Recommender trained and saved.")

    try:
        recommender = _load_model()
        st.success("Recommender loaded.")
    except Exception as exc:
        st.warning(str(exc))
        recommender = None

    users_df = _load_users()
    user_display = users_df[["code", "name", "company", "age"]].copy()
    user_display["label"] = (
        user_display["code"].astype(str)
        + " - "
        + user_display["name"]
        + " ("
        + user_display["company"]
        + ")"
    )
    selected_label = st.selectbox("Select user", user_display["label"].tolist())
    selected_user = int(selected_label.split(" - ")[0])

    top_n = st.slider("Recommendations", min_value=3, max_value=10, value=5)

with right:
    hotels_df = _load_hotels()

    st.subheader("User Profile")
    user_row = users_df[users_df["code"] == selected_user]
    st.dataframe(user_row, use_container_width=True)

    st.subheader("User Booking History")
    history = hotels_df[hotels_df["userCode"] == selected_user]
    if history.empty:
        st.info("No booking history found. Showing popular hotels.")
    st.dataframe(history[["name", "place", "days", "price", "total", "date"]], use_container_width=True)

    st.subheader("Recommended Hotels")
    if recommender:
        recs = recommend_for_user(recommender, selected_user, top_n=top_n)
        st.dataframe(recs, use_container_width=True)
    else:
        st.info("Train the recommender to get personalized suggestions.")

st.markdown("---")
st.subheader("Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.caption("Top Hotels by Bookings")
    top_hotels = (
        hotels_df.groupby("name", as_index=False)
        .agg(bookings=("travelCode", "count"))
        .sort_values("bookings", ascending=False)
        .head(10)
        .set_index("name")
    )
    st.bar_chart(top_hotels)

with col2:
    st.caption("Average Price by Place")
    avg_price_place = (
        hotels_df.groupby("place", as_index=False)
        .agg(avg_price=("price", "mean"))
        .sort_values("avg_price", ascending=False)
        .head(10)
        .set_index("place")
    )
    st.bar_chart(avg_price_place)

with col3:
    st.caption("Average Stay (days) by Place")
    avg_days_place = (
        hotels_df.groupby("place", as_index=False)
        .agg(avg_days=("days", "mean"))
        .sort_values("avg_days", ascending=False)
        .head(10)
        .set_index("place")
    )
    st.bar_chart(avg_days_place)
