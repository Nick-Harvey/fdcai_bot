from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import os

credentials_file = "../credentials.json"


class GoogleSheetsClient:
    def __init__(self, scopes, token_file, credentials_file):
        self.scopes = scopes
        self.token_file = token_file
        self.credentials_file = credentials_file
        self.creds = self.get_credentials()

    def get_credentials(self):
        # Get credentials for Google Sheets API
        creds = None
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.scopes)
                creds = flow.run_local_server(port=0)
            with open(self.token_file, "w") as token:
                token.write(creds.to_json())
        return creds

    def get_sheet_data(self, spreadsheet_id, range_name):
        # Fetch data from Google Sheets
        try:
            service = build("sheets", "v4", credentials=self.creds)
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
            return result
        except HttpError as err:
            print(err)
            return None

    @staticmethod
    def gsheet_to_dataframe(result):
        # Convert Google sheet data to DataFrame
        header = result.get("values", [])[0]
        values = result.get("values", [])[1:]
        if not values:
            print("No data found.")
            return None
        df = pd.DataFrame(values, columns=header)
        return df
