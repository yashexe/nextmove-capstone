import os
from dotenv import load_dotenv
import imaplib
import email
from email.header import decode_header

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

# Process and print the details of each email
for email_id in latest_emails:
    status, data = mail.fetch(email_id, "(RFC822)")
    msg = email.message_from_bytes(data[0][1])
    
    # Decode the subject
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8")
    
    # Decode the sender
    from_ = msg.get("From")
    
    # Print out the details
    print(f"Subject: {subject}")
    print(f"From: {from_}")
    print("="*50)

# Logout after fetching emails
mail.logout()
