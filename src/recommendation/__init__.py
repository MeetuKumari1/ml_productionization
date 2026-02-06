"""Recommendation package exports."""

from src.recommendation.recommender import (
    HOTELS_PATH,
    USERS_PATH,
    load_hotels,
    load_recommender,
    recommend_for_user,
    save_recommender,
    train_recommender,
)

__all__ = [
    "HOTELS_PATH",
    "USERS_PATH",
    "load_hotels",
    "load_recommender",
    "recommend_for_user",
    "save_recommender",
    "train_recommender",
]
