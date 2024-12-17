import pickle

# Load model and vectorizer
with open("machine_learning/models/naive_bayes.pkl", "rb") as model_file:
    model = pickle.load(model_file)
with open("machine_learning/models/tfidf_vectorizer.pkl", "rb") as vec_file:
    vectorizer = pickle.load(vec_file)

def predict_category(email_content):
    """
    Predict the category of an email using the pre-trained Naive Bayes model.
    Args:
        email_content (str): The content of the email.
    Returns:
        str: Predicted category.
    """
    email_tfidf = vectorizer.transform([email_content])
    return model.predict(email_tfidf)[0]

# Example usage
if __name__ == "__main__":
    email = "Huge sale happening this weekend! Don't miss out on 50% discounts."
    predicted_category = predict_category(email)
    print("Predicted Category:", predicted_category)
