import os
import gspread
from django.conf import settings
from google.oauth2.service_account import Credentials


def sync_application_to_sheet(application, remark=""):
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        creds_path = os.path.join(settings.BASE_DIR, "credentials.json")

        creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
        client = gspread.authorize(creds)

        sheet = client.open_by_key("1OYOj6T4d24dfAdF86Z9OGxxJWru_oRBB33X0oTQiVYI").sheet1
        customer = application.customer

        sheet.append_row([
            customer.name,
            customer.aadhaar_no,
            customer.contact_no,
            application.application_name,
            application.application_no,
            str(application.application_date),
            application.status,
            str(application.delivery_date) if application.delivery_date else "",
            remark,
        ])

        print("Google Sheet Sync Success")

    except Exception as e:
        print("Google Sheet Sync Error:", e)