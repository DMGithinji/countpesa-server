import os
import tempfile
import fitz  # PyMuPDF
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

def get_parsed_statement(parsered_file, password):
  pdf_data = get_pdf_text(parsered_file, password)
  text_content = pdf_data.get('text', None)

  parser = None
  for p in parsers:
      if p['identifier_substring'] in text_content:
        parser = p['parser']
        break
  if not parser:
    raise ValueError('The statement parsered is not handled yet. Please report this in the feedback section.')

  statement_list = text_content.split("\n")
  parsed_statement = parser(statement_list)
  return parsed_statement

def get_pdf_text(parsered_file, password):

  # Create a temporary file to save the parsered PDF
  with tempfile.NamedTemporaryFile(delete=False) as temp_pdf:
      for chunk in parsered_file.chunks():
          temp_pdf.write(chunk)

  # Open the temporary file to read its bytes
  with open(temp_pdf.name, 'rb') as f:
      pdf_bytes = f.read()

  try:
    pdf_reader = fitz.open(stream=pdf_bytes, filetype="pdf")
    pdf_reader.authenticate(password)

    if pdf_reader.is_encrypted:
      raise ValueError("Could not decrypt PDF.")
  except Exception as e:
    raise ValueError(f'{str(e)}')

  # Reading PDF content
  text_content = ''
  for page_number in range(len(pdf_reader)):
      page = pdf_reader[page_number]
      text_content += page.get_text("text")

  # Delete the temporary PDF file
  os.unlink(temp_pdf.name)
  return { 'text': text_content }
