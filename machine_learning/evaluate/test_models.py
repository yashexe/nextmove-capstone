import os
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from utils import (
    load_config,
    get_trained_logistic_regression_model,
    get_trained_naive_bayes_model,
    get_trained_tfidf_vectorizer,
    evaluate_model,
    save_evaluation_results,  # New import
)


def evaluate_pretrained_model(model, vectorizer, X, y, model_name, results_csv, clear_file=False):
    """
    Evaluate a pre-trained model on a test set and save results to CSV.
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

    # Save the results using the reusable function
    save_evaluation_results(results_csv, model_name, metrics, report, clear_file=clear_file)


if __name__ == "__main__":
    print("Loading configuration...")
    config = load_config()

    print("Loading pre-trained models and vectorizer...")
    logistic_regression_model = get_trained_logistic_regression_model()
    naive_bayes_model = get_trained_naive_bayes_model()
    tfidf_vectorizer = get_trained_tfidf_vectorizer()

    print("Loading test data...")
    data_path = config["data"]["processed_emails"]
    processed_data = pd.read_csv(data_path)
    X_test, y_test = processed_data["processed_content"], processed_data["category"]

    print("Evaluating models...")

    # Get path for saving results
    results_csv = config["results"]["model_results"]

    # Evaluate and save results
    evaluate_pretrained_model(
        logistic_regression_model, tfidf_vectorizer, X_test, y_test, 
        "Logistic Regression", results_csv, clear_file=True
        )
    evaluate_pretrained_model(
        naive_bayes_model, tfidf_vectorizer, X_test, y_test, 
        "Naive Bayes", results_csv)

    print(f"\nModel evaluation completed. Results saved to {results_csv}")