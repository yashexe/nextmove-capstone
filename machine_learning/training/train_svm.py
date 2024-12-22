import pandas as pd
from sklearn.svm import SVC
import pickle
from utils import load_config, validate_data


def train_svm(
    train_data_path, svm_kernel, svm_c, model_path, vectorizer_path
):
    """
    Train an SVM model using a pre-trained TF-IDF vectorizer.

    Args:
        train_data_path (str): Path to the training dataset.
        svm_kernel (str): Kernel type for the SVM (e.g., 'linear', 'rbf').
        svm_c (float): Regularization parameter for SVM.
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

    # --- Train SVM Model ---
    print(f"Training SVM model: kernel={svm_kernel}, C={svm_c}")
    model = SVC(kernel=svm_kernel, C=svm_c, probability=True)
    model.fit(X_train_tfidf, y_train)

    # --- Save Model ---
    print(f"Saving trained model to: {model_path}")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    print("SVM model training completed and saved successfully.")


if __name__ == "__main__":
    print("Loading configuration...")
    config = load_config()

    # Parse parameters from the config file
    train_data_path = config["paths"]["data"]["train_set"]  # Training dataset path
    svm_kernel = config["training"]["svm_kernel"]
    svm_c = config["training"]["svm_c"]
    model_path = config["paths"]["models"]["svm"]
    vectorizer_path = config["paths"]["models"]["tfidf_vectorizer"]

    # Call the function with parsed parameters
    print("Starting SVM training...")
    train_svm(
        train_data_path,
        svm_kernel,
        svm_c,
        model_path,
        vectorizer_path
    )
    print("SVM training completed successfully.")
