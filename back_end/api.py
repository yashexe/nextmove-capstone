import os
from dotenv import load_dotenv
import imaplib
import email
from email.header import decode_header
import json

# Load environment variables from .env file
load_dotenv()

# Connect to the IMAP server
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(os.getenv('EMAIL'), os.getenv('APP_PASSWORD'))

# Select the inbox (you can change this to any folder you want to read)
mail.select("inbox")

# Search for all emails
status, messages = mail.search(None, "ALL")

# Get the IDs of the most recent 5 emails
email_ids = messages[0].split()
latest_emails = email_ids[-5:]  # Get the last 5 email IDs

# Process and store the details of each email
emails = []
for email_id in latest_emails:
    status, data = mail.fetch(email_id, "(RFC822)")
    msg = email.message_from_bytes(data[0][1])
    
    # Decode the subject
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8")
    
    # Decode the sender
    from_ = msg.get("From")
    
    # Store email details
    emails.append({
        "subject": subject,
        "from": from_,
        "body": msg.get_payload(decode=True).decode(errors='ignore')
    })

# Save emails to a local JSON file (or could be used with localStorage in JavaScript)
with open('emails.json', 'w') as f:
    json.dump(emails, f, indent=4)

# Logout after fetching emails
mail.logout()
