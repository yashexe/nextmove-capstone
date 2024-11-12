import pickle

# Load the saved Naive Bayes model
with open('machine_learning/model/naive_bayes_model.pkl', 'rb') as model_file:
    nb_model = pickle.load(model_file)

# Load the saved TF-IDF vectorizer
with open('machine_learning/model/tfidf_vectorizer.pkl', 'rb') as vectorizer_file:
    tfidf = pickle.load(vectorizer_file)

def predict_category(email_content):
    """
    Predicts the category of a new email using the loaded Naive Bayes model and TF-IDF vectorizer.
    
    Args:
        email_content (str): The content of the email to classify.
    
    Returns:
        str: The predicted category of the email.
    """
    # Transform the email content using the loaded TF-IDF vectorizer
    email_tfidf = tfidf.transform([email_content])
    
    # Predict the category
    predicted_category = nb_model.predict(email_tfidf)
    
    return predicted_category[0]

# Example usage
if __name__ == "__main__":
    # Sample email content for prediction
    new_email = """ Exclusive Offer Inside – Just for You!"""

    # Predict the category
    predicted_category = predict_category(new_email)
    print(f"The predicted category for the email is: {predicted_category}")
