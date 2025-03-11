# server.py
from flask import Flask, jsonify
import imaplib
import email
from email.header import decode_header
import os
import pickle
from dotenv import load_dotenv
from utils import preprocess_text
import pickle

# Initialize Flask app
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

<<<<<<< HEAD
import os

print("Current working directory:", os.getcwd())

MODEL_PATH = os.path.abspath("C:\\github\\CAPSTONE\\nextmove-capstone\\machine_learning\\models\\logistic_regression.pkl")
VECTORIZER_PATH = os.path.abspath("C:\\github\\CAPSTONE\\nextmove-capstone\\machine_learning\\models\\tfidf_vectorizer.pkl")

print("Looking for model at:", MODEL_PATH)
print("File exists:", os.path.exists(MODEL_PATH))
print("Looking for vectorizer at:", VECTORIZER_PATH)
print("File exists:", os.path.exists(VECTORIZER_PATH))

print("Loading ML model...")
with open(MODEL_PATH, 'rb') as model_file:
    model = pickle.load(model_file)
print("Model loaded successfully!")

print("Loading vectorizer...")
with open(VECTORIZER_PATH, 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)
print("Vectorizer loaded successfully!")

def categorize_email(subject):
    """Predicts the category of an email using the trained ML model."""
    subject_vectorized = vectorizer.transform([subject])
    predicted_category = model.predict(subject_vectorized)[0]
    print(f"Subject: {subject} → Predicted Category: {predicted_category}")
    return predicted_category
=======

# Calculate paths relative to the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ML_MODELS_DIR = os.path.join(BASE_DIR, '..', 'machine_learning', 'models')

# Paths to the model and vectorizer files
vectorizer_path = os.path.join(ML_MODELS_DIR, 'tfidf_vectorizer.pkl')
model_path = os.path.join(ML_MODELS_DIR, 'naive_bayes.pkl')

# Load the TF-IDF vectorizer
with open(vectorizer_path, 'rb') as f:
    vectorizer = pickle.load(f)

# Load the Naive Bayes model
with open(model_path, 'rb') as f:
    ml_model = pickle.load(f)

>>>>>>> fc2f95b9cd2ad2f294f905c6aaf6ada048170ab6

@app.route('/update-emails')
def update_emails():
    """Fetches and categorizes emails from Gmail."""
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(os.getenv('EMAIL'), os.getenv('APP_PASSWORD'))
    mail.select("inbox")  # Select the inbox

    status, messages = mail.search(None, "ALL")
    email_ids = messages[0].split()
    latest_emails = email_ids[-30:]  # Get the last 5 email IDs

    categorized_emails = {}

    for email_id in latest_emails:
        status, data = mail.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])

        # Decode subject
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")
        from_ = msg.get("From")

<<<<<<< HEAD
        # Categorize the email using ML model
        category = categorize_email(subject)
        if category not in categorized_emails:
            categorized_emails[category] = []
        categorized_emails[category].append({
=======
        # Use ML model to classify the email based on its subject.
        # (For now we’re only classifying using the subject.)
        category = classify_email(subject)

        emails.append({
>>>>>>> fc2f95b9cd2ad2f294f905c6aaf6ada048170ab6
            "subject": subject,
            "from": from_,
            "category": category
        })

    mail.logout()  # Logout after fetching emails
<<<<<<< HEAD
    return jsonify(categorized_emails)  # Return categorized emails
=======

    return jsonify(emails)  # Return emails as JSON, now including the predicted category.

def classify_email(text):
    # Preprocess the input text to mimic training data's 'processed_content'
    preprocessed_text = preprocess_text(text)
    # Transform the preprocessed text using the loaded TF-IDF vectorizer
    features = vectorizer.transform([preprocessed_text])
    # Predict the category using the loaded Naive Bayes model
    prediction = ml_model.predict(features)
    return prediction[0]
>>>>>>> fc2f95b9cd2ad2f294f905c6aaf6ada048170ab6

if __name__ == "__main__":
    app.run(debug=True)
