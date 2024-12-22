import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from utils import load_config


def train_and_save_vectorizer(data_path, tfidf_max_features, tfidf_ngram_range, vectorizer_path):
    """
    Train a TF-IDF vectorizer and save it to a file.
    Args:
        data_path (str): Path to the processed data file.
        tfidf_max_features (int): Maximum number of features for TF-IDF.
        tfidf_ngram_range (tuple): N-gram range for TF-IDF.
        vectorizer_path (str): Path to save the TF-IDF vectorizer.
    """
    print(f"Loading data from: {data_path}")
    data = pd.read_csv(data_path)
    X = data['processed_content']

    print(f"Training TF-IDF vectorizer: max_features={tfidf_max_features}, ngram_range={tfidf_ngram_range}")
    tfidf = TfidfVectorizer(max_features=tfidf_max_features, ngram_range=tfidf_ngram_range)
    tfidf.fit(X)

    print(f"Saving vectorizer to: {vectorizer_path}")
    with open(vectorizer_path, "wb") as f:
        pickle.dump(tfidf, f)

    print("Vectorizer trained and saved successfully.")


if __name__ == "__main__":
    print("Loading configuration...")
    config = load_config()

    # Define paths and parameters
    train_data_path = config["paths"]["data"]["train_set"]
    vectorizer_path = config["paths"]["models"]["tfidf_vectorizer"]
    tfidf_max_features = config["training"]["tfidf_max_features"]
    tfidf_ngram_range = tuple(config["training"]["tfidf_ngram_range"])

    train_and_save_vectorizer(train_data_path, tfidf_max_features, tfidf_ngram_range, vectorizer_path)
