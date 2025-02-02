import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from utils import (
    load_config,
    get_trained_tfidf_vectorizer,
    get_trained_logistic_regression_model,
    get_trained_naive_bayes_model,
    get_trained_svm_model,
    evaluate_model,
    save_evaluation_results,
)


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


if __name__ == "__main__":
    print("Loading configuration...")
    config = load_config()

    print("Loading pre-trained models and vectorizer...")
    tfidf_vectorizer = get_trained_tfidf_vectorizer()
    logistic_regression_model = get_trained_logistic_regression_model()
    naive_bayes_model = get_trained_naive_bayes_model()
    svm_model = get_trained_svm_model()

    print("Loading test data...")
    test_data_path = config["paths"]["data"]["test_set"]  # Load test dataset path from config
    test_data = pd.read_csv(test_data_path)
    X_test, y_test = test_data["processed_content"], test_data["label"]

    print("Evaluating models...")
    # Get path for saving results
    results_csv = config["paths"]["results"]["model_results"]

    # Evaluate and save results
    evaluate_pretrained_model(
        logistic_regression_model, tfidf_vectorizer, X_test, y_test, 
        "Logistic Regression", results_csv, clear_file=True
    )
    evaluate_pretrained_model(
        naive_bayes_model, tfidf_vectorizer, X_test, y_test, 
        "Naive Bayes", results_csv
    )
    evaluate_pretrained_model(
        svm_model, tfidf_vectorizer, X_test, y_test, 
        "SVM", results_csv
    )

    print(f"\nModel evaluation completed. Results saved to {results_csv}")
