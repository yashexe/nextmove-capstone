import pandas as pd
import torch
from sklearn.metrics import classification_report, confusion_matrix
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from utils import (
    load_config,
    get_trained_tfidf_vectorizer,
    get_trained_logistic_regression_model,
    get_trained_naive_bayes_model,
    get_trained_svm_model,
    evaluate_model,
    save_evaluation_results,
)

# Load configuration at the global level
CONFIG = load_config()

# Extract paths and parameters
TEST_DATA_PATH = CONFIG["paths"]["data"]["test_set"]
RESULTS_CSV_PATH = CONFIG["paths"]["results"]["model_results"]
DISTILBERT_MODEL_PATH = CONFIG["paths"]["models"]["distilbert"]["checkpoints"]
DISTILBERT_TOKENIZER_PATH = CONFIG["paths"]["models"]["distilbert"]["tokenizer"]

def evaluate_pretrained_model(model, vectorizer, X, y, model_name, results_csv, clear_file=False):
    """
    Evaluate a pre-trained model on a test set and save results to CSV.

    Args:
        model: Pre-trained model to evaluate.
        vectorizer: TF-IDF vectorizer to transform input data.
        X (pd.Series): Test input data.
        y (pd.Series): Test labels.
        model_name (str): Name of the model for logging.
        results_csv (str): Path to save evaluation results.
        clear_file (bool): Whether to clear the CSV file before saving.
    """
    print(f"\nEvaluating {model_name}...")
    X_tfidf = vectorizer.transform(X)
    y_pred = model.predict(X_tfidf)

    # Calculate evaluation metrics
    metrics = evaluate_model(y, y_pred)
    report = classification_report(y, y_pred, output_dict=True)

    # Display metrics
    print(f"{model_name} Performance Metrics:")
    print(f"Accuracy: {metrics['accuracy']:.2f}")
    print("Classification Report:")
    print(pd.DataFrame(report).transpose())
    print("Confusion Matrix:")
    print(confusion_matrix(y, y_pred))

    # Save the results
    save_evaluation_results(results_csv, model_name, metrics, report, clear_file=clear_file)


def evaluate_distilbert(model_path, tokenizer_path, test_data_path, results_csv, clear_file=False):
    """
    Evaluate a fine-tuned DistilBERT model on the test set.

    Args:
        model_path (str): Path to the fine-tuned model.
        tokenizer_path (str): Path to the tokenizer files.
        test_data_path (str): Path to the test dataset.
        results_csv (str): Path to save evaluation results.
        clear_file (bool): Whether to clear the CSV file before saving.
    """
    print("Loading test data...")
    test_data = pd.read_csv(test_data_path)
    X_test, y_test = test_data["processed_content"], test_data["label"]

    print("Loading model and tokenizer...")
    model = DistilBertForSequenceClassification.from_pretrained(model_path)
    tokenizer = DistilBertTokenizer.from_pretrained(tokenizer_path)

    # Move model to appropriate device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    model.to(device)
    model.eval()

    print("Tokenizing test data...")
    test_encodings = tokenizer(
        list(X_test),
        truncation=True,
        padding=True,
        max_length=512,
        return_tensors="pt"
    )
    test_encodings = {key: val.to(device) for key, val in test_encodings.items()}

    print("Making predictions...")
    with torch.no_grad():
        outputs = model(**test_encodings)
        y_pred = torch.argmax(outputs.logits, dim=1).cpu().numpy()

    # Map predicted labels back to string categories
    label_mapping = {0: "Work", 1: "Personal", 2: "Promotional", 3: "Urgent"}
    y_pred_strings = [label_mapping[label] for label in y_pred]

    # Ensure true labels are strings
    if pd.api.types.is_numeric_dtype(y_test):
        reverse_label_mapping = {v: k for k, v in label_mapping.items()}
        y_test = y_test.map(reverse_label_mapping)

    # Evaluate predictions
    print("Evaluating model...")
    metrics = evaluate_model(y_test, y_pred_strings)
    report = classification_report(y_test, y_pred_strings, output_dict=True)

    # Display metrics
    print(f"DistilBERT Performance Metrics:")
    print(f"Accuracy: {metrics['accuracy']:.2f}")
    print("Classification Report:")
    print(pd.DataFrame(report).transpose())
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred_strings, labels=list(label_mapping.values())))

    # Save the results
    save_evaluation_results(results_csv, "DistilBERT", metrics, report, clear_file=clear_file)
    print(f"Results saved to {results_csv}")



if __name__ == "__main__":
    print("Loading pre-trained models and vectorizer...")
    tfidf_vectorizer = get_trained_tfidf_vectorizer()
    logistic_regression_model = get_trained_logistic_regression_model()
    naive_bayes_model = get_trained_naive_bayes_model()
    svm_model = get_trained_svm_model()

    print("Loading test data...")
    test_data = pd.read_csv(TEST_DATA_PATH)
    X_test, y_test = test_data["processed_content"], test_data["label"]

    print("Evaluating models...")
    # Evaluate traditional models
    evaluate_pretrained_model(
        logistic_regression_model, tfidf_vectorizer, X_test, y_test, 
        "Logistic Regression", RESULTS_CSV_PATH, clear_file=True
    )
    evaluate_pretrained_model(
        naive_bayes_model, tfidf_vectorizer, X_test, y_test, 
        "Naive Bayes", RESULTS_CSV_PATH
    )
    evaluate_pretrained_model(
        svm_model, tfidf_vectorizer, X_test, y_test, 
        "SVM", RESULTS_CSV_PATH
    )

    # Evaluate DistilBERT
    evaluate_distilbert(
        DISTILBERT_MODEL_PATH,
        DISTILBERT_TOKENIZER_PATH,
        TEST_DATA_PATH,
        RESULTS_CSV_PATH
    )

    print(f"\nModel evaluation completed. Results saved to {RESULTS_CSV_PATH}")
