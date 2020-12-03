from __future__ import print_function
import pickle
import os.path
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1Q_m6U2DQkeSDEM-Ow6L9D_BjdvPto3TTzf6wxWX38jI'
RANGE_NAME = 'Detailed Review!A5:E'

class quickStartClass:
    def __init__(self) -> None:
        self.reviewer = {}
        self.sa = {}
        self.account_name = {}
        self.ein_tin_ssn = {}
        self.count = 0

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
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)


    def main(self):
        """ Uses Googles Sheets API to grab data from 
        sheet and detect any changes since last grab.
        """

        # Call the Sheets API
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            print(f'current loop: {self.count}')

        self.count = self.count + 1
        for row, column in enumerate(values):
            if self.count == 1:
                self.reviewer[row] = (values[row][1])
                self.sa[row] = (values[row][2])
                self.account_name[row] = (values[row][3])
                self.ein_tin_ssn[row] = (values[row][4])
            else:
                if self.reviewer[row] == values[row][1]:
                    # if this happens, then nothing has changed, append value and continue
                    pass
                else:
                    print(f'-----there was a change for value reviewer!-----\n-----previous value: {self.reviewer[row]} || current value: {values[row][1]}-----')
                    self.reviewer[row] = (values[row][1])
                if self.sa[row] == values[row][2]:
                    # if this happens, then nothing has changed, append value and continue
                    pass
                else:
                    print(f'-----there was a change for value SA!-----\n-----previous value: {self.sa[row]} || current value: {values[row][2]}-----')
                    self.sa[row] = (values[row][2])
                if self.account_name[row] == values[row][3]:
                    # if this happens, then nothing has changed, append value and continue
                    pass
                else:
                    print(f'-----there was a change for value account name!-----\n-----previous value: {self.account_name[row]} || current value: {values[row][3]}-----')
                    self.account_name[row] = (values[row][3])
                if self.ein_tin_ssn[row] == values[row][4]:
                    # if this happens, then nothing has changed, append value and continue
                    pass
                else:
                    print(f'-----there was a change for value ein tin ssn!-----\n-----previous value: {self.ein_tin_ssn[row]} || current value: {values[row][4]}-----')
                    self.ein_tin_ssn[row] = (values[row][4])



if __name__ == '__main__':
    c = quickStartClass()

    while(True):
        # sleep 5 seconds between each data pull
        time.sleep(5)
        c.main()


