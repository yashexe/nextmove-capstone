# test_app.py
import email
from unittest.mock import patch, MagicMock
import pytest
from server import app  

# Test when there are more than 5 emails available.
@patch('server.imaplib.IMAP4_SSL')  # Updated patch target
def test_update_emails_more_than_five(mock_imap):
    # Create a fake IMAP instance.
    instance = MagicMock()
    mock_imap.return_value = instance

    # Simulate successful login and selection.
    instance.login.return_value = ('OK', [b'Logged in'])
    instance.select.return_value = ('OK', [b''])

    # Simulate search returning 10 email IDs.
    instance.search.return_value = ('OK', [b'1 2 3 4 5 6 7 8 9 10'])

    # For each fetch, create a dummy email with a unique subject.
    def fetch_side_effect(email_id, message_parts):
        email_num = email_id.decode()  # e.g., b'6' -> "6"
        raw_email = (
            f"Subject: Test email {email_num}\n"
            "From: sender@example.com\n"
            "\n"
            "This is a test email."
        )
        msg = email.message_from_string(raw_email)
        return ('OK', [(None, msg.as_bytes())])

    instance.fetch.side_effect = fetch_side_effect
    instance.logout.return_value = ('OK', [b'Logged out'])

    # Use the Flask test client to make a request.
    with app.test_client() as client:
        response = client.get('/update-emails')
        data = response.get_json()

    # We expect exactly 5 emails to be returned (the last 5 of 10).
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 5

    # Since the last five email IDs are: 6, 7, 8, 9, 10, verify each subject.
    expected_ids = [b'6', b'7', b'8', b'9', b'10']
    for i, email_item in enumerate(data):
        expected_subject = f"Test email {expected_ids[i].decode()}"
        assert email_item['subject'] == expected_subject
        assert email_item['from'] == "sender@example.com"


# Test when fewer than 5 emails are available.
@patch('server.imaplib.IMAP4_SSL')
def test_update_emails_less_than_five(mock_imap):
    instance = MagicMock()
    mock_imap.return_value = instance

    instance.login.return_value = ('OK', [b'Logged in'])
    instance.select.return_value = ('OK', [b''])

    # Simulate search returning 3 email IDs.
    instance.search.return_value = ('OK', [b'1 2 3'])

    def fetch_side_effect(email_id, message_parts):
        email_num = email_id.decode()
        raw_email = (
            f"Subject: Test email {email_num}\n"
            "From: sender@example.com\n"
            "\n"
            "This is a test email."
        )
        msg = email.message_from_string(raw_email)
        return ('OK', [(None, msg.as_bytes())])

    instance.fetch.side_effect = fetch_side_effect
    instance.logout.return_value = ('OK', [b'Logged out'])

    with app.test_client() as client:
        response = client.get('/update-emails')
        data = response.get_json()

    # Since there are only 3 emails, the endpoint should return all 3.
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 3

    expected_ids = [b'1', b'2', b'3']
    for i, email_item in enumerate(data):
        expected_subject = f"Test email {expected_ids[i].decode()}"
        assert email_item['subject'] == expected_subject
        assert email_item['from'] == "sender@example.com"


# Test when no emails are available.
@patch('server.imaplib.IMAP4_SSL')
def test_update_emails_empty(mock_imap):
    instance = MagicMock()
    mock_imap.return_value = instance

    instance.login.return_value = ('OK', [b'Logged in'])
    instance.select.return_value = ('OK', [b''])

    # Simulate search returning an empty result.
    instance.search.return_value = ('OK', [b''])
    instance.logout.return_value = ('OK', [b'Logged out'])

    with app.test_client() as client:
        response = client.get('/update-emails')
        data = response.get_json()

    # Expect an empty list when no emails are found.
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 0
