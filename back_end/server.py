from flask import Flask, jsonify, request
from flask_cors import CORS
import imaplib
import email
from email.header import decode_header
import os
import pickle
from dotenv import load_dotenv
from config import EMAIL
from bs4 import BeautifulSoup
import bleach
import re

app = Flask(__name__)
CORS(app)

registered_users = set()
load_dotenv()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
MODEL_PATH = os.path.join(PROJECT_ROOT, "machine_learning", "models", "logistic_regression.pkl")
VECTORIZER_PATH = os.path.join(PROJECT_ROOT, "machine_learning", "models", "tfidf_vectorizer.pkl")

# Load trained model and vectorizer
with open(MODEL_PATH, 'rb') as model_file:
    model = pickle.load(model_file)
with open(VECTORIZER_PATH, 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

def categorize_email(subject, body):
    combined_text = f"{subject} {body}"
    text_vectorized = vectorizer.transform([combined_text])
    predicted_category = model.predict(text_vectorized)[0]
    return predicted_category

def sanitize_html(html):
    html = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'[\u200b-\u200f\u202a-\u202e\u2060-\u206f\ufeff]+', '', html)
    clean = bleach.clean(
        html,
        tags=bleach.sanitizer.ALLOWED_TAGS + ['p', 'br', 'div', 'span', 'a', 'strong', 'em', 'ul', 'li'],
        attributes={
            'a': ['href', 'title'],
            'img': ['src', 'alt', 'style'],
            '*': ['style']
        },
        strip=True
    )
    clean = re.sub(r'<(p|div|span)>\s*</\1>', '', clean)
    clean = re.sub(r'(<br\s*/?>\s*){3,}', '<br><br>', clean)
    clean = re.sub(r'(\n\s*){3,}', '\n\n', clean)
    return clean


@app.route('/update-emails')
def update_emails():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(os.getenv('EMAIL'), os.getenv('APP_PASSWORD'))
    mail.select("inbox")

    status, messages = mail.search(None, "ALL")
    email_ids = messages[0].split()[-100:]

    categorized_emails = {}

    for email_id in email_ids:
        status, data = mail.fetch(email_id, "(RFC822 X-GM-MSGID)")
        msg = email.message_from_bytes(data[0][1])

        gm_msg_id = None
        for part in data:
            if isinstance(part, tuple):
                raw_header = part[0].decode(errors="ignore")
                match = re.search(r'X-GM-MSGID (\d+)', raw_header)
                if match:
                    gm_msg_id = match.group(1)

        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")
        from_ = msg.get("From")

        body = "Unable to Read Body"
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if content_type == "text/html" and "attachment" not in content_disposition:
                    raw_html = part.get_payload(decode=True).decode(errors="ignore")
                    body = sanitize_html(raw_html)
                    break
                elif content_type == "text/plain" and not body:
                    body = part.get_payload(decode=True).decode(errors="ignore")
        else:
            content_type = msg.get_content_type()
            if content_type == "text/html":
                raw_html = msg.get_payload(decode=True).decode(errors="ignore")
                body = sanitize_html(raw_html)
            elif content_type == "text/plain":
                body = msg.get_payload(decode=True).decode(errors="ignore")

        category = categorize_email(subject, body)
        if category not in categorized_emails:
            categorized_emails[category] = []

        categorized_emails[category].append({
            "subject": subject,
            "from": from_,
            "category": category,
            "body": body,
            "gmail_id": gm_msg_id
        })

    mail.logout()
    return jsonify(categorized_emails)

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
