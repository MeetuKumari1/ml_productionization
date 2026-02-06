"""Hotel recommender utilities based on item-item similarity."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

HOTELS_PATH = Path("travel_capstone/hotels.csv")
USERS_PATH = Path("travel_capstone/users.csv")
ARTIFACT_PATH = Path("artifacts/hotel_recommender.joblib")
METADATA_PATH = Path("artifacts/hotel_recommender_metadata.json")

Recommender = dict[str, Any]


def load_hotels(data_path: str | Path = HOTELS_PATH) -> pd.DataFrame:
    path = Path(data_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    return pd.read_csv(path)


def build_recommender(df: pd.DataFrame) -> Recommender:
    if df[["userCode", "name"]].isna().any().any():
        raise ValueError("Missing values in userCode/name.")

    interactions = pd.crosstab(df["userCode"], df["name"])
    user_ids = interactions.index.to_list()
    hotel_names = interactions.columns.to_list()

    # Compute item-item similarity based on booking interactions.
    item_matrix = interactions.T.values
    item_similarity = cosine_similarity(item_matrix)

    # Aggregate popularity and pricing for fallback recommendations.
    hotel_stats = (
        df.groupby(["name", "place"], as_index=False)
        .agg(bookings=("travelCode", "count"), avg_price=("price", "mean"))
        .sort_values(["bookings", "avg_price"], ascending=[False, True])
    )

    return {
        "user_ids": user_ids,
        "hotel_names": hotel_names,
        "item_similarity": item_similarity,
        "interactions": interactions,
        "hotel_stats": hotel_stats,
    }


def save_recommender(recommender: Recommender) -> dict:
    ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(recommender, ARTIFACT_PATH)

    metadata = {
        "artifact_path": str(ARTIFACT_PATH),
        "num_users": len(recommender["user_ids"]),
        "num_hotels": len(recommender["hotel_names"]),
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return metadata


def train_recommender(data_path: str | Path = HOTELS_PATH) -> dict:
    df = load_hotels(data_path)
    recommender = build_recommender(df)
    return save_recommender(recommender)


def load_recommender() -> Recommender:
    if not ARTIFACT_PATH.exists():
        raise FileNotFoundError(
            f"Recommender artifact not found at {ARTIFACT_PATH}. "
            "Run train_recommender() first."
        )
    return joblib.load(ARTIFACT_PATH)


def recommend_for_user(
    recommender: Recommender,
    user_code: int,
    top_n: int = 5,
) -> pd.DataFrame:
    interactions = recommender["interactions"]
    hotel_stats = recommender["hotel_stats"]
    hotel_names = recommender["hotel_names"]
    item_similarity = recommender["item_similarity"]

    if user_code not in interactions.index:
        return hotel_stats.head(top_n)

    user_vector = interactions.loc[user_code].values
    scores = user_vector @ item_similarity
    seen_mask = user_vector > 0
    scores = scores.astype(float)
    scores[seen_mask] = -np.inf

    top_idx = np.argsort(scores)[::-1][:top_n]
    recommended_hotels = [hotel_names[i] for i in top_idx]

    return hotel_stats[hotel_stats["name"].isin(recommended_hotels)]
