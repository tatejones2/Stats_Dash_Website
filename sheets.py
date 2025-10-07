import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Replace with your actual Google Sheets ID and range
SHEET_ID = "13d-isMNuVnqEXRw3ASll2FMK6lw4Ar8odPN4l9Txa0o"
RANGE_NAME = "Dash!B1:BQ22"
CREDENTIALS_FILE = "credentials.json"  # Place your credentials file in the project


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
        
        # Handle mixed header structure
        headers = values[0]  # First row
        
        # Create generic headers for columns B-I (columns 0-7 in the data)
        for i in range(8):  # B through I (8 columns)
            if i >= len(headers) or not headers[i]:
                if i < len(headers):
                    headers[i] = f"Column_{chr(66+i)}"  # B, C, D, etc.
                else:
                    headers.append(f"Column_{chr(66+i)}")
        
        # Handle duplicate column names by adding suffixes
        seen_names = {}
        unique_headers = []
        for header in headers:
            if header in seen_names:
                seen_names[header] += 1
                unique_headers.append(f"{header}_{seen_names[header]}")
            else:
                seen_names[header] = 0
                unique_headers.append(header)
        
        # Ensure all data rows have the same number of columns as headers
        data_rows = []
        for row in values[1:]:
            # Pad row to match header length
            padded_row = row + [''] * (len(unique_headers) - len(row))
            data_rows.append(padded_row)
        
        data_frame = pd.DataFrame(data_rows, columns=unique_headers)
        return data_frame
    except FileNotFoundError as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error fetching data: {e}")
        return None
