import os
import pickle
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource

from app.configuration import CNF


class GmailClient:
    def __init__(self):
        self.service = self._build_service(self._authorize())

    @staticmethod
    def _authorize(credentials_file: str = CNF.CREDENTIALS_FILE, scopes: List[str] = CNF.SCOPES) -> Credentials:
        credentials = None
        # The file token.pickle stores the user's access and refresh tokens, and is created automatically when the
        # authorization flow completes for the first time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                credentials = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
                credentials = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(credentials, token)

        return credentials

    @staticmethod
    def _build_service(credentials: Credentials) -> Resource:
        return build('gmail', 'v1', credentials=credentials)

    def get_labels(self) -> None:
        results = self.service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
        else:
            print('Labels:')
            for label in labels:
                print(label['name'])
