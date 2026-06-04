import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def read_google_sheet():

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json",
        scope
    )

    client = gspread.authorize(credentials)

    sheet = client.open(
        "Daily Water Usage and Issue Report (Dormitory) (Responses)"
    ).worksheet(
        "Form Responses 1"
    )

    data = sheet.get_all_records()

    return pd.DataFrame(data)