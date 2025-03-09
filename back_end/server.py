from flask import Flask, jsonify
import imaplib
import email
from email.header import decode_header
import os
import pickle
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

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

        # Categorize the email using ML model
        category = categorize_email(subject)
        if category not in categorized_emails:
            categorized_emails[category] = []
        categorized_emails[category].append({
            "subject": subject,
            "from": from_,
        })

    mail.logout()  # Logout after fetching emails
    return jsonify(categorized_emails)  # Return categorized emails

if __name__ == "__main__":
    app.run(debug=True)
