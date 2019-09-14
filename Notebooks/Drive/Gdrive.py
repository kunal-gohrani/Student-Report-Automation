import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
if __name__=='__main__':
    import GDriveAuthenticator
import io
class Gdrive:
    def __init__(self,creds):
        self.__creds=creds
        self.drive_service = build('drive', 'v3', credentials=self.__creds)
    def search(self,searchfor,**kwargs):
        query_string="name='{0}'".format(searchfor) #and mimeType='application/vnd.google-apps.spreadsheet'".format(searchfor)
        page_token = None
        while True:
            response = self.drive_service.files().list(q=query_string,\
                                            fields='nextPageToken, files(id,name,mimeType)',\
                                            pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change
                print('Found file:',file.get('name'),'(',file.get('id'),file.get('mimeType'),')')
                return tuple((file.get('name'),file.get('id')))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
            
    def download(self,name='Student Gradebook.xlsx',fileid='1HYjfEe3aCbufbqIXKs0Xz-gfoQNztGhCN1ivx0gZXnc'):
        request = self.drive_service.files().export_media(fileId=fileid,
                                             mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        fh = io.FileIO('Student Gradebook.xlsx','wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download.", int(status.progress() * 100))
if __name__=='__main__':
    g=GDriveAuthenticator.GDriveAuthenticator('client_secret.json')
    creds=g.authenticate()
    f=Gdrive(creds)
    name,fileid=f.search('Student Gradebook')
    f.download(name=name,fileid=fileid)



