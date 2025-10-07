import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Replace with your actual Google Sheets ID and range
SHEET_ID = "YOUR_SHEET_ID"
RANGE_NAME = "Sheet1!A1:Z1000"
CREDENTIALS_FILE = "path/to/credentials.json"  # Place your credentials file in the project


def fetch_sheet_data():
    """Fetch data from Google Sheets and return as DataFrame."""
    try:
        creds = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
        )
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()  # pylint: disable=no-member
        result = sheet.values().get(spreadsheetId=SHEET_ID, range=RANGE_NAME).execute()
        values = result.get("values", [])
        if not values:
            return None
        data_frame = pd.DataFrame(values[1:], columns=values[0])
        return data_frame
    except FileNotFoundError as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error fetching data: {e}")
        return None
