import os
import gspread
from datetime import datetime


def get_credentials() -> dict:
  """
  Return gspread credentials.
  """
  return {
    "type": os.environ.get('TYPE', ''),
    "project_id": os.environ.get('PROJECT_ID', ''),
    "private_key_id": os.environ.get('PRIVATE_KEY_ID', ''),
    "private_key": os.environ.get('PRIVATE_KEY', ''),
    "client_email": os.environ.get('CLIENT_EMAIL', ''),
    "client_id": os.environ.get('CLIENT_ID', ''),
    "auth_uri": os.environ.get('AUTH_URI', ''),
    "token_uri": os.environ.get('TOKEN_URI', ''),
    "auth_provider_x509_cert_url": os.environ.get('AUTH_PROVIDER_X509_CERT_URL', ''),
    "client_x509_cert_url": os.environ.get('CLIENT_X509_CERT_URL', ''),
    "universe_domain": os.environ.get('UNIVERSE_DOMAIN', ''),
  }

def get_worksheet(workSheetType):
  """
  Initialize a gspread client with the given credentials.
  """
  worksheet = {
    "feedback": "CountpesaFeedback",
    "chatpesa": "ChatPesa: Failed Prompts"
  }
  gc = gspread.service_account_from_dict(get_credentials())
  spreadsheet = gc.open(worksheet[workSheetType])
  worksheet = spreadsheet.sheet1
  return worksheet


def post_feedback_data(data):
  """
  Posts feedback data to Google Sheet worksheet.
  """
  current_datetime = datetime.now()
  formatted_datetime = current_datetime.strftime('%d %b %Y, %I:%M %p')
  post_content = {
    'source': data.get('url', None),
    'message': data.get('message', None),
    'type': data.get('feedbackType', None),
    'date': formatted_datetime
  }
  values = [post_content[key] for key in post_content]
  worksheet = get_worksheet('feedback')
  worksheet.append_row(values)


def post_failed_chatpesa_questions(question, response):
  """
  Posts email to to Google Sheet worksheet.
  """
  current_datetime = datetime.now()
  formatted_datetime = current_datetime.strftime('%d %b %Y, %I:%M %p')
  values = [formatted_datetime, question]
  if response:
    values.append(response)

  worksheet = get_worksheet('chatpesa')
  worksheet.append_row(values)
