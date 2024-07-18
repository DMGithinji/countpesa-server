import os
import tempfile
import fitz  # PyMuPDF
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError, PermissionDenied

from .safaricom_app import safaricom_app_parser
# from .mpesa_app_parser import mpesa_app_parser

parsers = [
  {
    'identifier_substring': 'M-PESA STATEMENT',
    'parser': safaricom_app_parser
  },
  # {
  #   'identifier_substring': 'MPESA FULL STATEMENT',
  #   'parser': mpesa_app_parser
  # }
]

def get_parsed_statement(statement: UploadedFile, password: str) -> dict:
  pdf_data = get_pdf_text(statement, password)
  text_content = pdf_data.get('text', None)

  parser = None
  for p in parsers:
      if p['identifier_substring'] in text_content:
        parser = p['parser']
        break
  if not parser:
    raise ValidationError('The statement type uploaded is not handled yet. Please report this in the feedback section.')

  statement_list = text_content.split("\n")
  parsed_statement = parser(statement_list)
  return parsed_statement

def get_pdf_text(statement: UploadedFile, password: str) -> dict:

  # Create a temporary file to save the parsered PDF
  with tempfile.NamedTemporaryFile(delete=False) as temp_pdf:
      for chunk in statement.chunks():
          temp_pdf.write(chunk)

  # Open the temporary file to read its bytes
  with open(temp_pdf.name, 'rb') as f:
      pdf_bytes = f.read()

  pdf_reader = fitz.open(stream=pdf_bytes, filetype="pdf")
  pdf_reader.authenticate(password)

  if pdf_reader.is_encrypted:
    raise PermissionDenied("Could not decrypt PDF.")

  # Reading PDF content
  text_content = ''
  for page_number in range(len(pdf_reader)):
      page = pdf_reader[page_number]
      text_content += page.get_text("text")

  # Delete the temporary PDF file
  os.unlink(temp_pdf.name)
  return { 'text': text_content }
