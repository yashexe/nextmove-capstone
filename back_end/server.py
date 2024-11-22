from flask import Flask, jsonify
import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

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

        # Only append subject and sender, ignoring the body
        emails.append({
            "subject": subject,
            "from": from_,
        })

    mail.logout()  # Logout after fetching emails

    return jsonify(emails)  # Return emails as JSON, without body content

if __name__ == "__main__":
    app.run(debug=True)

