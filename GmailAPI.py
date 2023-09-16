import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']


def get_gmail_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'config.py', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)


def send_email(service, to_email, subject, message):
    email_content = MIMEText(message, 'plain')
    email_content['to'] = to_email
    email_content['subject'] = subject
    raw_email = base64.urlsafe_b64encode(
        email_content.as_bytes()).decode('utf-8')
    send_message = service.users().messages().send(
        userId='me', body={'raw': raw_email}).execute()
    return send_message


def list_emails(service, query=''):
    results = service.users().messages().list(userId='me', q=query).execute()
    return results.get('messages', [])


def read_email(service, email_id):
    email_data = service.users().messages().get(userId='me', id=email_id).execute()
    return email_data
