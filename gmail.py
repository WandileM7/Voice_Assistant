import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from events import *

def get_gmail_service():
    """
    Authenticate and build the Gmail service.

    Returns:
        googleapiclient.discovery.Resource: The authenticated Gmail service.
    """
    creds = authenticate_google()
    return build('gmail', 'v1', credentials=creds)

def read_emails(num_emails=5):
    """
    Read the specified number of recent emails from the user's Gmail inbox.

    Args:
        num_emails (int, optional): The number of emails to read. Defaults to 5.

    Returns:
        str: A summary of the read emails or an error message.
    """
    try:
        service = get_gmail_service()
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=num_emails).execute()
        messages = results.get('messages', [])

        emails = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            email_data = {}
            email_data['id'] = msg['id']
            email_data['snippet'] = msg['snippet']

            for header in msg['payload']['headers']:
                if header['name'] == 'Subject':
                    email_data['subject'] = header['value']
                if header['name'] == 'From':
                    email_data['sender'] = header['value']

            emails.append(email_data)

        # Convert the list of emails to a string format
        email_summary = "\n".join(
            [f"From: {email['sender']}, Subject: {email['subject']}, Snippet: {email['snippet']}" for email in emails]
        )
        return email_summary
    except HttpError as error:
        return f'An error occurred: {error}'

def send_email(to, subject, body):
    """
    Send an email using the authenticated Gmail service.

    Args:
        to (str): The recipient's email address.
        subject (str): The subject of the email.
        body (str): The body content of the email.

    Returns:
        str: A message indicating the result of the operation or an error message.
    """
    try:
        service = get_gmail_service()
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
        send_message = (service.users().messages().send(userId="me", body=create_message).execute())
        return f'Message Id: {send_message["id"]}'
    except HttpError as error:
        return f'An error occurred: {error}'
