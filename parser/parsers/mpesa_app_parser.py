import re
from .helpers import convert_to_datetime


def mpesa_app_parser(STATEMENT_LIST):
  """
  Extracts all transactions from a statement downloaded from MPESA APP

  Parameters:
  STATEMENT_LIST (list of str): A list of string values extracted from the statement

  Note: Is not reliable however, since the statements from MPESA APP can have issues such as:
  - No transaction description
  - Duplicated transactions.
  """
  STATEMENT_DICT = { index: value for index, value in enumerate(STATEMENT_LIST) }

  def retrieve_transaction_details(status_index):
    """ returns a single transaction dict given the index of the transaction's completion status"""
    # handle getting amount and balance from text after the 'COMPLETED' value in row
    amounts = " ".join([STATEMENT_DICT[status_index + 1], STATEMENT_DICT[status_index + 2], STATEMENT_DICT[status_index + 3]])
    extracted_amounts = extract_amounts(amounts)
    paid_in = extracted_amounts[0]
    withdrawn = -extracted_amounts[1]
    balance = extracted_amounts[2]
    amount = paid_in if paid_in != 0 else withdrawn

    # handle getting transaction description, date and code from text before the 'COMPLETED' value in row
    pointer = status_index - 1
    transaction_description = ''
    while (not extract_date_and_text(STATEMENT_DICT[pointer])['date']):
      cleaned_vals = extract_date_and_text(STATEMENT_DICT[pointer])
      transaction_description = cleaned_vals['substring'] + ' ' + transaction_description
      pointer -= 1
    # Set date and add the last text portion
    cleaned_vals = extract_date_and_text(STATEMENT_DICT[pointer])
    transaction_description = cleaned_vals['substring'] + ' ' + transaction_description
    trasaction_date = convert_to_datetime(cleaned_vals['date'])

    return {
      'mpesa_code': STATEMENT_DICT[pointer - 1],
      'trasaction_date': trasaction_date,
      'transaction_description': transaction_description.strip(),
      'status': STATEMENT_DICT[status_index],
      'amount': amount,
      'balance': balance
    }

  parsed_statement = {
    'transactions': []
  }

  for index, text in enumerate(STATEMENT_LIST):
    if text == 'COMPLETED':
      transaction = retrieve_transaction_details(index)
      parsed_statement['transactions'].append(transaction)

  return parsed_statement

def extract_date_and_text(s):
    # Regex pattern to match the date and time at the beginning of the string
    match = re.match(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})(.*)", s)
    if match:
        date_value = match.group(1).strip()
        substring = match.group(2).strip()
    else:
        date_value = None
        substring = s.strip()

    return {"date": date_value, "substring": substring}

def extract_amounts(input_string):
    # Regex to find numbers with optional commas and a required decimal point
    matches = re.findall(r'\d{1,3}(?:,\d{3})*(?:\.\d{2})?', input_string)
    # Convert the first three matched numbers to floats after removing commas
    return [float(num.replace(',', '')) for num in matches[:3]]
