from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

def list_files(username, doc_type='Variant', subject='M_'):
    """
    Lists files from Google Drive that match the given username and subject.

    Args:
        username (str): The username to search for in the file names.
        subject (str): The subject to search for in the file names.

    Returns:
        list: A list of file names that match the given username and subject.
    """
    WHAT_TO_FIND = {
        'Variant': f'name contains "{subject}" and name contains "{username}" and name contains ".pdf"',
        'Homework': f'name contains "Overall" and name contains "{username}" and name contains ".pdf"',
        'Files': f'name contains "I_F_" and name contains "{username}" and name contains ".zip"' 
    }

    SCOPES = ['https://www.googleapis.com/auth/drive']

    creds = None
    if os.path.exists('access_files/token.json'):
        creds = Credentials.from_authorized_user_file('access_files/token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('path_to_your_client_secrets_file.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('access_files/token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the service
    service = build('drive', 'v3', credentials=creds)

    # Search for files
    results = service.files().list(pageSize=100, fields="nextPageToken, files(name)",
                                    q=WHAT_TO_FIND[doc_type]).execute()
    items = results.get('files', [])

    return [elem['name'] for elem in items]
