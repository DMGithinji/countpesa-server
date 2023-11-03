import os
import gspread
from typing import List
from django.conf import settings


def get_credentials() -> dict:
  """
  Return gspread credentials.
  """
  return {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY"),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN")
  }


def get_worksheet() -> gspread.client.Client:
  """
  Initialize a gspread client with the given credentials.
  """
  gc = gspread.service_account_from_dict(get_credentials())
  spreadsheet = gc.open('CountpesaFeedback')
  worksheet = spreadsheet.sheet1
  return worksheet

def post_data(data):
  """
  Posts feedback data to Google Sheet worksheet.
  """
  post_content = {
    'type': data.get('feedbackType', None),
    'message': data.get('message', None),
    'source': data.get('url', None)
  }

  values = [post_content[key] for key in post_content]

  worksheet = get_worksheet()

  worksheet.append_row(values)
