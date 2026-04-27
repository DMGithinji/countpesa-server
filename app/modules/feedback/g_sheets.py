from datetime import datetime
import logging

import gspread

from app.config import google_credentials, settings

logger = logging.getLogger(__name__)


def get_worksheet(google_sheet):
    gc = gspread.service_account_from_dict(google_credentials)
    spreadsheet = gc.open(google_sheet)
    return spreadsheet.sheet1


def post_feedback_data(data):
    current_datetime = datetime.now(settings.TIMEZONE)
    formatted_datetime = current_datetime.strftime("%d %b %Y, %I:%M %p")
    post_content = {
        "date": formatted_datetime,
        "message": data.get("message", None),
        "type": data.get("type", None),
        "email": data.get("email", None),
    }
    values = [post_content[key] for key in post_content]
    # Keep empty fields blank in Sheets instead of literal "None".
    values = ["" if value is None else value for value in values]
    worksheet = get_worksheet(data.get("google_sheet_name"))
    # Avoid Google Sheets "table detection" surprises by writing to the actual last row.
    next_row = len(worksheet.get_all_values()) + 1
    end_column = chr(ord("A") + len(values) - 1)
    worksheet.update(f"A{next_row}:{end_column}{next_row}", [values])
    logger.info(
        "Feedback appended to sheet '%s' at row %s",
        data.get("google_sheet_name"),
        next_row,
    )
