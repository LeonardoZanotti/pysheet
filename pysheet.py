#!/usr/bin/env python3
# Leonardo José Zanotti
# https://github.com/LeonardoZanotti/pysheet
from __future__ import print_function

import os.path
from math import ceil

from decouple import config
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = config("SPREADSHEET_ID")
SAMPLE_RANGE_NAME = "C4:G"
UPDATE_RANGE = "G4:H"
CLASSES_RANGE = "A2"


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
        .execute()
    )
    values = result.get("values", [])

    if not values:
        print("No data found.")
    else:
        classes_result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=CLASSES_RANGE)
            .execute()
        )
        classes = int(classes_result.get("values", [])[0][0].split(": ")[1])

        updated_values = list()

        for row in values:
            # Average calc
            average = ceil((int(row[1]) + int(row[2]) + int(row[3])) / 3)
            score_needed = 0

            if average < 50:
                situation = "Reprovado por Nota"
            elif average >= 70:
                situation = "Aprovado"
            else:
                situation = "Exame Final"
                score_needed = 100 - average

            # class misses calc
            if int(row[0]) / classes > 0.25:
                situation = "Reprovado por Falta"
                score_needed = 0

            updated_values.append([situation, score_needed])

        # Update the cells
        body = {"values": updated_values}
        result = (
            sheet.values()
            .update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range=UPDATE_RANGE,
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )
        print("{0} cells updated.".format(result.get("updatedCells")))


if __name__ == "__main__":
    main()
