# server.py
from flask import Flask, jsonify
import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
from utils import preprocess_text
import pickle

# Initialize Flask app
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()


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


@app.route('/update-emails')
def update_emails():
    # Connect to the IMAP server and fetch emails
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(os.getenv('EMAIL'), os.getenv('APP_PASSWORD'))
    mail.select("inbox")  # Select the inbox

    # Fetch the most recent 5 emails
    status, messages = mail.search(None, "ALL")
    email_ids = messages[0].split()
    latest_emails = email_ids[-5:]  # Get the last 5 email IDs

    emails = []
    for email_id in latest_emails:
        status, data = mail.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])

        # Decode subject and sender
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")
        from_ = msg.get("From")

        # Use ML model to classify the email based on its subject.
        # (For now we’re only classifying using the subject.)
        category = classify_email(subject)

        emails.append({
            "subject": subject,
            "from": from_,
            "category": category
        })

    mail.logout()  # Logout after fetching emails

    return jsonify(emails)  # Return emails as JSON, now including the predicted category.

def classify_email(text):
    # Preprocess the input text to mimic training data's 'processed_content'
    preprocessed_text = preprocess_text(text)
    # Transform the preprocessed text using the loaded TF-IDF vectorizer
    features = vectorizer.transform([preprocessed_text])
    # Predict the category using the loaded Naive Bayes model
    prediction = ml_model.predict(features)
    return prediction[0]

if __name__ == "__main__":
    app.run(debug=True)

