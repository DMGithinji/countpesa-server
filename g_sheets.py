import os
from datetime import datetime
import gspread
from dotenv import load_dotenv

load_dotenv()

def get_credentials() -> dict:
    private_key = os.environ.get('PRIVATE_KEY', '').replace('\\n', '\n').replace('"', '')
    return {
        "type": os.environ.get('TYPE', ''),
        "project_id": os.environ.get('PROJECT_ID', ''),
        "private_key_id": os.environ.get('PRIVATE_KEY_ID', ''),
        "private_key": private_key,
        "client_email": os.environ.get('CLIENT_EMAIL', ''),
        "client_id": os.environ.get('CLIENT_ID', ''),
        "auth_uri": os.environ.get('AUTH_URI', ''),
        "token_uri": os.environ.get('TOKEN_URI', ''),
        "auth_provider_x509_cert_url": os.environ.get('AUTH_PROVIDER_X509_CERT_URL', ''),
        "client_x509_cert_url": os.environ.get('CLIENT_X509_CERT_URL', ''),
        "universe_domain": os.environ.get('UNIVERSE_DOMAIN', ''),
    }

def get_worksheet(google_sheet):
    gc = gspread.service_account_from_dict(get_credentials())
    spreadsheet = gc.open(google_sheet)
    return spreadsheet.sheet1

def post_feedback_data(data):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%d %b %Y, %I:%M %p')
    post_content = {
        'date': formatted_datetime,
        'message': data.get('message', None),
        'type': data.get('type', None),
        'email': data.get('email', None),
    }
    values = [post_content[key] for key in post_content]
    worksheet = get_worksheet(data.get('google_sheet'))
    worksheet.append_row(values)
