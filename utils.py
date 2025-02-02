import csv
import json
import os
import pickle
from typing import Counter
import pandas as pd
import yaml
import spacy
from spacy.cli import download

# Ensure the spaCy model is available
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Model 'en_core_web_sm' not found. Downloading...")
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def load_config(config_path="config.yaml"):
    """
    Load configuration from a YAML file. Resolves the path relative to the project root.
    """
    project_root = os.path.dirname(os.path.abspath(__file__))  # Path to utils.py
    config_full_path = os.path.join(project_root, config_path)
    with open(config_full_path, "r") as file:
        return yaml.safe_load(file)
    

def validate_data(data: pd.DataFrame, required_columns: list):
    """
    Validates the dataset.
    Checks that all required cols are present.
    Checks that no rows have missing data.

    Args:
        data (pd.DataFrame): The dataset to validate.
        required_columns (list): List of column names that must be present and have no missing values.

    Raises:
        ValueError: If required columns are missing or contain missing values.
    """
    # --- Check for Missing Columns ---
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    # --- Check for Missing Values in Required Columns ---
    for col in required_columns:
        if data[col].isnull().any():
            missing_rows = (data[data[col].isnull()].index + 2).tolist()  # One-based indexing
            raise ValueError(f"Missing values detected in '{col}' at rows: {missing_rows}")

    print("Validation passed: All required columns are present, and no missing values found.")


def validate_dataset(input_file=None):
    """
    Validates the structure and contents of a dataset file.

    Assumes the dataset contains the following structure:
    - Required keys: ['id', 'date', 'from', 'to', 'subject', 'body', 'label', 'reasoning', 'target_scenario']
    - Expected data types:
        - 'id': int
        - 'date': str
        - 'from': str
        - 'to': str
        - 'subject': str
        - 'body': str
        - 'label': str
        - 'reasoning': str
        - 'target_scenario': str

    Args:
        input_file (str, optional): Path to the JSON dataset file. If None, defaults to the path in config.yaml.

    Returns:
        bool: True if the dataset is valid, raises ValueError otherwise.
    """
    # Load config and get the default dataset path if input_file is not provided
    if input_file is None:
        from utils import load_config  # Ensure load_config is accessible
        config = load_config()
        input_file = config["paths"]["data"]["dataset"]
        print(f"Using dataset path from config: {input_file}")

    # Define the required keys and their expected types
    required_keys = ["id", "date", "from", "to", "subject", "body", "label", "reasoning", "target_scenario"]
    expected_types = {
        "id": int,
        "date": str,
        "from": str,
        "to": str,
        "subject": str,
        "body": str,
        "label": str,
        "reasoning": str,
        "target_scenario": str,
    }

    # Check if the file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"File not found at {input_file}")

    # Load the JSON file
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"Loaded dataset with {len(data)} entries.")
    except Exception as e:
        raise ValueError(f"Error loading JSON file: {e}")

    # Validate each entry
    inconsistencies = []
    category_counts = Counter()
    for i, entry in enumerate(data, start=1):
        entry_issues = []

        # Check for missing keys
        for key in required_keys:
            if key not in entry:
                entry_issues.append(f"Missing key: '{key}'")
            elif entry[key] is None:
                entry_issues.append(f"Key '{key}' is None")

        # Check for type mismatches
        for key, expected_type in expected_types.items():
            if key in entry and entry[key] is not None:
                if not isinstance(entry[key], expected_type):
                    entry_issues.append(f"Key '{key}' has incorrect type: Expected {expected_type}, got {type(entry[key])}")

        # Count categories if the 'label' key exists and is valid
        if "label" in entry and entry["label"] is not None and isinstance(entry["label"], str):
            category_counts[entry["label"]] += 1

        # Log issues for this entry
        if entry_issues:
            inconsistencies.append(f"Entry {i}: {', '.join(entry_issues)}")

    # Print or raise errors if inconsistencies exist
    if inconsistencies:
        print("\nInconsistencies found:")
        for issue in inconsistencies:
            print(issue)
        raise ValueError("Dataset validation failed. See inconsistencies above.")

    print("Validation passed: All required columns are present, and no missing values found.")

    # Print category counts
    print("\nCategory Counts:")
    for category, count in category_counts.items():
        print(f"  {category}: {count}")

    return True


def get_trained_tfidf_vectorizer():
    """
    Load the pre-trained TF-IDF vectorizer.
    """
    config = load_config()
    project_root = os.path.dirname(os.path.abspath(__file__))
    vectorizer_path = os.path.join(project_root, config["paths"]["models"]["tfidf_vectorizer"])
    with open(vectorizer_path, "rb") as file:
        return pickle.load(file)


def get_trained_logistic_regression_model():
    """
    Load the pre-trained Logistic Regression model.
    """
    config = load_config()
    project_root = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(project_root, config["paths"]["models"]["logistic_regression"])
    with open(model_path, "rb") as file:
        return pickle.load(file)


def get_trained_naive_bayes_model():
    """
    Load the pre-trained Naive Bayes model.
    """
    config = load_config()
    project_root = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(project_root, config["paths"]["models"]["naive_bayes"])
    with open(model_path, "rb") as file:
        return pickle.load(file)


def get_trained_svm_model():
    """
    Load the pre-trained SVM model.
    """
    config = load_config()
    project_root = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(project_root, config["paths"]["models"]["svm"])
    with open(model_path, "rb") as file:
        return pickle.load(file)


def preprocess_text(text):
    """
    Preprocesses text by tokenizing, lemmatizing, and retaining key parts of speech.

    - Converts text to lowercase.
    - Tokenizes and lemmatizes text.
    - Retains nouns, verbs, adjectives, and adverbs for context.
    - Keeps stopwords for better flow and removes irrelevant tokens.

    Args:
        text (str): The text to preprocess.

    Returns:
        str: Preprocessed text with richer context.
    """
    doc = nlp(text.lower())
    # Retain key parts of speech and allow meaningful stopwords for context
    clean_text = " ".join([
        token.text for token in doc
        if (token.is_alpha and 
            (token.is_stop or token.pos_ in {"NOUN", "VERB", "ADJ", "ADV"}))
    ])
    return clean_text


def evaluate_model(y_true, y_pred):
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
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

