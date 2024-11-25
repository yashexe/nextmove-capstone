import imaplib
import os
from dotenv import load_dotenv

load_dotenv()

mail = imaplib.IMAP4_SSL('imap.gmail.com')
try:
    mail.login(os.getenv('EMAIL'), os.getenv('APP_PASSWORD'))
    print("Login successful")
except imaplib.IMAP4.error as e:
    print(f"IMAP login failed: {e}")
