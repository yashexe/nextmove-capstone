import pickle

# Load model and vectorizer
with open("machine_learning/models/logistic_regression.pkl", "rb") as model_file:
    model = pickle.load(model_file)
with open("machine_learning/models/tfidf_vectorizer.pkl", "rb") as vec_file:
    vectorizer = pickle.load(vec_file)

def predict_category(email_content):
    """Predict the category of an email."""
    email_tfidf = vectorizer.transform([email_content])
    return model.predict(email_tfidf)[0]

# Example usage
if __name__ == "__main__":
    email = "Reminder: Submit the report by EOD."
    print("Predicted Category:", predict_category(email))
