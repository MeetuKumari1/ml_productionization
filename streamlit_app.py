"""Streamlit UI for hotel recommendations and insights."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.recommendation.recommender import (
    HOTELS_PATH,
    USERS_PATH,
    load_hotels,
    load_recommender,
    recommend_for_user,
    train_recommender,
)

st.set_page_config(page_title="Travel Hotel Recommendations", layout="wide")


@st.cache_data
def _load_users() -> pd.DataFrame:
    return pd.read_csv(USERS_PATH)


@st.cache_data
def _load_hotels() -> pd.DataFrame:
    return load_hotels(HOTELS_PATH)


@st.cache_resource
def _load_model():
    return load_recommender()


def _build_user_labels(users_df: pd.DataFrame) -> pd.DataFrame:
    display_df = users_df[["code", "name", "company", "age"]].copy()
    display_df["label"] = (
        display_df["code"].astype(str)
        + " - "
        + display_df["name"]
        + " ("
        + display_df["company"]
        + ")"
    )
    return display_df


def _render_left_panel(users_df: pd.DataFrame):
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

    user_display = _build_user_labels(users_df)
    selected_label = st.selectbox("Select user", user_display["label"].tolist())
    selected_user = int(selected_label.split(" - ")[0])
    top_n = st.slider("Recommendations", min_value=3, max_value=10, value=5)
    return selected_user, top_n, recommender


def _render_user_profile(users_df: pd.DataFrame, user_code: int) -> None:
    st.subheader("User Profile")
    user_row = users_df[users_df["code"] == user_code]
    st.dataframe(user_row, use_container_width=True)


def _render_history(hotels_df: pd.DataFrame, user_code: int) -> None:
    st.subheader("User Booking History")
    history = hotels_df[hotels_df["userCode"] == user_code]
    if history.empty:
        st.info("No booking history found. Showing popular hotels.")
    st.dataframe(
        history[["name", "place", "days", "price", "total", "date"]],
        use_container_width=True,
    )


def _render_recommendations(
    recommender,
    user_code: int,
    top_n: int,
) -> None:
    st.subheader("Recommended Hotels")
    if recommender:
        recs = recommend_for_user(recommender, user_code, top_n=top_n)
        st.dataframe(recs, use_container_width=True)
        return
    st.info("Train the recommender to get personalized suggestions.")


def _render_insights(hotels_df: pd.DataFrame) -> None:
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


st.title("Hotel Recommendations & Insights")

users_df = _load_users()
hotels_df = _load_hotels()

left, right = st.columns([1, 2])
with left:
    selected_user, top_n, recommender = _render_left_panel(users_df)

with right:
    _render_user_profile(users_df, selected_user)
    _render_history(hotels_df, selected_user)
    _render_recommendations(recommender, selected_user, top_n)

_render_insights(hotels_df)
