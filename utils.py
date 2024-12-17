import csv
import os
import pickle
import yaml

def load_config(config_path="config.yaml"):
    """
    Load configuration from a YAML file. Resolves the path relative to the project root.
    """
    project_root = os.path.dirname(os.path.abspath(__file__))  # Path to utils.py
    config_full_path = os.path.join(project_root, config_path)
    with open(config_full_path, "r") as file:
        return yaml.safe_load(file)

def get_trained_logistic_regression_model():
    """
    Load the pre-trained Logistic Regression model.
    """
    config = load_config()
    project_root = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(project_root, config["model"]["logistic_regression"])
    with open(model_path, "rb") as file:
        return pickle.load(file)

def get_trained_naive_bayes_model():
    """
    Load the pre-trained Naive Bayes model.
    """
    config = load_config()
    project_root = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(project_root, config["model"]["naive_bayes"])
    with open(model_path, "rb") as file:
        return pickle.load(file)

def get_trained_tfidf_vectorizer():
    """
    Load the pre-trained TF-IDF vectorizer.
    """
    config = load_config()
    project_root = os.path.dirname(os.path.abspath(__file__))
    vectorizer_path = os.path.join(project_root, config["model"]["tfidf_vectorizer"])
    with open(vectorizer_path, "rb") as file:
        return pickle.load(file)


# 3. Evaluation Metrics Function
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def evaluate_model(y_true, y_pred):
    """
    Evaluate model performance using standard metrics.

    Args:
        y_true (list): True labels.
        y_pred (list): Predicted labels.

    Returns:
        dict: Evaluation metrics (accuracy, precision, recall, F1-score).
    """
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, average="weighted"),
        "recall": recall_score(y_true, y_pred, average="weighted"),
        "f1_score": f1_score(y_true, y_pred, average="weighted"),
    }
    return metrics

import os
import csv

def save_evaluation_results(results_csv, model_name, metrics, report, clear_file=False):
    """
    Save evaluation results to a CSV file.

    Args:
        results_csv (str): Path to the results CSV file.
        model_name (str): Name of the evaluated model.
        metrics (dict): Dictionary of evaluation metrics (accuracy).
        report (dict): Classification report dictionary.
        clear_file (bool): Whether to clear the file before writing results.
    """
    # Ensure the results directory exists
    os.makedirs(os.path.dirname(results_csv), exist_ok=True)

    # Clear the file by overwriting it with a header (only if clear_file=True)
    if clear_file:
        with open(results_csv, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Model", "Accuracy", "Precision", "Recall", "F1-Score"])

    # Write or append results to the CSV file
    with open(results_csv, mode="a", newline="") as file:
        writer = csv.writer(file)
        # Write a header if the file is empty
        if file.tell() == 0:
            writer.writerow(["Model", "Accuracy", "Precision", "Recall", "F1-Score"])

        # Append metrics to the CSV file
        writer.writerow([
            model_name,
            metrics['accuracy'],
            report['weighted avg']['precision'],
            report['weighted avg']['recall'],
            report['weighted avg']['f1-score'],
        ])

