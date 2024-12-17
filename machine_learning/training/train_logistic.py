import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
from utils import load_config


def train_and_evaluate_logistic_regression(
    data_path, test_size, random_state, tfidf_max_features, tfidf_ngram_range,
    logistic_max_iter, model_path, vectorizer_path
):
    """
    Train and evaluate a Logistic Regression model.
    Args:
        data_path (str): Path to the processed data file.
        test_size (float): Proportion of data to use as the test set.
        random_state (int): Random state for reproducibility.
        tfidf_max_features (int): Maximum number of features for TF-IDF.
        tfidf_ngram_range (tuple): N-gram range for TF-IDF.
        logistic_max_iter (int): Maximum iterations for Logistic Regression.
        model_path (str): Path to save the trained model.
        vectorizer_path (str): Path to save the TF-IDF vectorizer.
    """
    # --- Load Data ---
    print(f"Loading data from: {data_path}")
    data = pd.read_csv(data_path)
    X, y = data['processed_content'], data['category']

    # --- Split Data ---
    print(f"Splitting data: test_size={test_size}, random_state={random_state}")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # --- Vectorize Data ---
    print(f"Vectorizing data: max_features={tfidf_max_features}, ngram_range={tfidf_ngram_range}")
    tfidf = TfidfVectorizer(max_features=tfidf_max_features, ngram_range=tfidf_ngram_range)
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)

    # --- Train Logistic Regression Model ---
    print(f"Training Logistic Regression model: max_iter={logistic_max_iter}")
    model = LogisticRegression(max_iter=logistic_max_iter)
    model.fit(X_train_tfidf, y_train)

    # --- Evaluate the Model ---
    y_pred = model.predict(X_test_tfidf)
    print("\nModel Evaluation:")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    # --- Save Model and Vectorizer ---
    print(f"Saving model to: {model_path}")
    print(f"Saving vectorizer to: {vectorizer_path}")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    with open(vectorizer_path, "wb") as f:
        pickle.dump(tfidf, f)

    print("\nModel and vectorizer saved successfully.")


if __name__ == "__main__":
    print("Loading configuration...")
    config = load_config()

    # Parse parameters from the config file
    data_path = config["data"]["processed_emails"]
    test_size = config["training"]["test_size"]
    random_state = config["training"]["random_state"]
    tfidf_max_features = config["training"]["tfidf_max_features"]
    tfidf_ngram_range = tuple(config["training"]["tfidf_ngram_range"])
    logistic_max_iter = config["training"]["logistic_regression_max_iter"]
    model_path = config["model"]["logistic_regression"]
    vectorizer_path = config["model"]["tfidf_vectorizer"]

    # Call the function with parsed parameters
    print("Starting Logistic Regression training and evaluation...")
    train_and_evaluate_logistic_regression(
        data_path,
        test_size,
        random_state,
        tfidf_max_features,
        tfidf_ngram_range,
        logistic_max_iter,
        model_path,
        vectorizer_path
    )
    print("Training and evaluation completed successfully.")
