import pickle

# Load the saved Logistic Regression model
with open('machine_learning/model/logistic_regression_model.pkl', 'rb') as model_file:
    logreg_model = pickle.load(model_file)

# Load the saved TF-IDF vectorizer
with open('machine_learning/model/tfidf_vectorizer.pkl', 'rb') as vectorizer_file:
    tfidf = pickle.load(vectorizer_file)

def predict_category(email_content):
    """
    Predicts the category of a new email using the loaded Logistic Regression model and TF-IDF vectorizer.
    
    Args:
        email_content (str): The content of the email to classify.
    
    Returns:
        str: The predicted category of the email.
    """
    # Transform the email content using the loaded TF-IDF vectorizer
    email_tfidf = tfidf.transform([email_content])
    
    # Predict the category
    predicted_category = logreg_model.predict(email_tfidf)
    
    return predicted_category[0]

# Example usage
if __name__ == "__main__":
    # Sample email content for prediction
    new_email = """ Reminder: Submit the project report by EOD today. Check your calendar for meeting timings. """

    # Predict the category
    predicted_category = predict_category(new_email)
    print(f"The predicted category for the email is: {predicted_category}")


    #  Run Command python .\machine_learning\model\predict_with_logistic.py in \nextmove-capstone> 
