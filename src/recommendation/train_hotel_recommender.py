# from recommendation.recommender import train_recommender
from recommender import train_recommender



def main():
    metadata = train_recommender()
    print("Recommender trained and saved.")
    print(metadata)


if __name__ == "__main__":
    main()
