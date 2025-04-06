# server.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import imaplib
import email
from email.header import decode_header
import os
import pickle
from dotenv import load_dotenv
import pickle
from config import EMAIL
from bs4 import BeautifulSoup

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Create a set of registerd userss
registered_users = set()


# Load environment variables from .env file
load_dotenv()



print("Current working directory:", os.getcwd())

# Get the current file directory (server.py location)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up to project root from back_end
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
# Define model paths relative to root
MODEL_PATH = os.path.join(PROJECT_ROOT, "machine_learning", "models", "logistic_regression.pkl")
VECTORIZER_PATH = os.path.join(PROJECT_ROOT, "machine_learning", "models", "tfidf_vectorizer.pkl")

print("Model Path:", MODEL_PATH)
print("Vectorizer Path:", VECTORIZER_PATH)

print("Looking for model at:", MODEL_PATH)
print("File exists:", os.path.exists(MODEL_PATH))
print("Looking for vectorizer at:", VECTORIZER_PATH)
print("File exists:", os.path.exists(VECTORIZER_PATH))

print("Loading ML model...")
with open(MODEL_PATH, 'rb') as model_file: model = pickle.load(model_file)
print("Model loaded successfully!")

print("Loading vectorizer...")
with open(VECTORIZER_PATH, 'rb') as vectorizer_file: vectorizer = pickle.load(vectorizer_file)
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
    latest_emails = email_ids[-100:]  # Get the last 5 email IDs

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
        
        body = "Unable to Read Body"
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if content_type == "text/plain" and "attachment" not in content_disposition:
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
                elif content_type == "text/html" and not body:
                    html = part.get_payload(decode=True).decode(errors="ignore")
                    body = BeautifulSoup(html, "html.parser").get_text()
        else:
            content_type = msg.get_content_type()
            if content_type == "text/plain":
                body = msg.get_payload(decode=True).decode(errors="ignore")
            elif content_type == "text/html":
                html = msg.get_payload(decode=True).decode(errors="ignore")
                body = BeautifulSoup(html, "html.parser").get_text()

        categorized_emails[category].append({
            "subject": subject,
            "from": from_,
            "category": category,
            "body": body
        })

    mail.logout()  # Logout after fetching emails
    return jsonify(categorized_emails)  # Return categorized emails

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    if email != EMAIL:
        return jsonify({'error': 'Email does not match the allowed admin email'}), 403

    if email in registered_users:
        return jsonify({'error': 'Email already registered'}), 409

    registered_users.add(email)
    return jsonify({'message': 'Registration successful'}), 200


if __name__ == "__main__":
    app.run(debug=True)
