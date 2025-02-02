import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle
from utils import load_config, validate_data


def train_logistic_regression(
    train_data_path, logistic_max_iter, model_path, vectorizer_path
):
    """
    Train a Logistic Regression model using a pre-trained TF-IDF vectorizer.

    Args:
        train_data_path (str): Path to the training dataset.
        logistic_max_iter (int): Maximum iterations for Logistic Regression.
        model_path (str): Path to save the trained model.
        vectorizer_path (str): Path to load the pre-trained TF-IDF vectorizer.
    """
    # --- Load Training Data ---
    print(f"Loading training data from: {train_data_path}")
    train_data = pd.read_csv(train_data_path)

    # --- Validate Data ---
    validate_data(train_data, required_columns=['processed_content', 'label'])  # Ensure data is valid

    X_train, y_train = train_data['processed_content'], train_data['label']

    # --- Load Pre-trained Vectorizer ---
    print(f"Loading pre-trained vectorizer from: {vectorizer_path}")
    with open(vectorizer_path, "rb") as f:
        tfidf = pickle.load(f)

    # --- Transform Data ---
    print("Transforming training data using the pre-trained vectorizer...")
    X_train_tfidf = tfidf.transform(X_train)

    # --- Train Logistic Regression Model ---
    print(f"Training Logistic Regression model: max_iter={logistic_max_iter}")
    model = LogisticRegression(max_iter=logistic_max_iter)
    model.fit(X_train_tfidf, y_train)

    # --- Save Model ---
    print(f"Saving trained model to: {model_path}")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    print("Logistic Regression model training completed and saved successfully.")


if __name__ == "__main__":
    print("Loading configuration...")
    config = load_config()

    # Parse parameters from the config file
    train_data_path = config["paths"]["data"]["train_set"]  # Training dataset path
    logistic_max_iter = config["training"]["logistic_regression_max_iter"]
    model_path = config["paths"]["models"]["logistic_regression"]
    vectorizer_path = config["paths"]["models"]["tfidf_vectorizer"]

    # Call the function with parsed parameters
    print("Starting Logistic Regression training...")
    train_logistic_regression(
        train_data_path,
        logistic_max_iter,
        model_path,
        vectorizer_path
    )
    print("Logistic Regression training completed successfully.")
