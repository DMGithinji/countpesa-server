from datetime import datetime

import gspread

from app.config import google_credentials


def get_worksheet(google_sheet):
    gc = gspread.service_account_from_dict(google_credentials)
    spreadsheet = gc.open(google_sheet)
    return spreadsheet.sheet1


def post_feedback_data(data):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d %b %Y, %I:%M %p")
    post_content = {
        "date": formatted_datetime,
        "message": data.get("message", None),
        "type": data.get("type", None),
        "email": data.get("email", None),
    }
    values = [post_content[key] for key in post_content]
    worksheet = get_worksheet(data.get("google_sheet_name"))
    worksheet.append_row(values)
