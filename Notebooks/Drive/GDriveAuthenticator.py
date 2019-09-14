#from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES='https://www.googleapis.com/auth/drive'
class GDriveAuthenticator:
    def __init__(self,CLIENT_SECRET):
        self.SCOPE='https://www.googleapis.com/auth/drive'
        self.CLIENT_SECRET=CLIENT_SECRET
    def authenticate(self):
        """Authenticates the application with the google account and returns the
        credentials acquired"""

        creds = None
        
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CLIENT_SECRET, self.SCOPE)

                try:
                    creds = flow.run_local_server(port=0)
                    print('\nAuthentication successful!')
                except:
                    print('Some problem in authentication, please retry!')
                    return

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds