"""CLI entrypoint to train and persist the hotel recommender."""

from src.recommendation.recommender import train_recommender


def main() -> None:
    metadata = train_recommender()
    print("Recommender trained and saved.")
    print(metadata)


if __name__ == "__main__":
    main()
