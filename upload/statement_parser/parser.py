import re
from .utils import is_date_string, convert_to_number, convert_to_datetime

def parse_statement_text(STATEMENT_LIST):
  # STATEMENT_LIST = text_content.split("\n")
  STATEMENT_DICT = { index: value for index, value in enumerate(STATEMENT_LIST) }

  def get_next(curr_index):
    return STATEMENT_DICT[curr_index + 1]

  def get_paid_in_and_out(curr_index):
    return {
      'paid_in': convert_to_number(STATEMENT_DICT[curr_index + 1]),
      'paid_out': convert_to_number(STATEMENT_DICT[curr_index + 2])
    }

  def retrieve_transaction_details(transaction_date_index):
    transaction_description = ''
    pointer = transaction_date_index + 1
    while (STATEMENT_DICT.get(pointer) and STATEMENT_DICT[pointer] != 'Completed'):
      transaction_description += f'{STATEMENT_DICT[pointer]} '
      pointer += 1
    return {
      'mpesa_code': STATEMENT_DICT[transaction_date_index - 1],
      'trasaction_date': STATEMENT_DICT[transaction_date_index],
      'transaction_description': transaction_description.strip(),
      'status': STATEMENT_DICT[pointer],
      'amount': convert_to_number(STATEMENT_DICT[pointer + 1]),
      'balance': convert_to_number(STATEMENT_DICT[pointer + 2])
    }

  actions = {
    'Customer Name:': get_next,
    'Mobile Number:': get_next,
    'Email Address:': get_next,
    'Statement Period:': get_next,
    'Request Date:': get_next,

    'SEND MONEY:': get_paid_in_and_out,
    'RECEIVED MONEY:': get_paid_in_and_out,
    'AGENT DEPOSIT:': get_paid_in_and_out,
    'AGENT WITHDRAWAL:': get_paid_in_and_out,
    'LIPA NA M-PESA (PAYBILL):': get_paid_in_and_out,
    'LIPA NA M-PESA (BUY GOODS):': get_paid_in_and_out,
    'OTHERS:': get_paid_in_and_out,
    'TOTAL:': get_paid_in_and_out,
  }

  parsed_statement = {
    'metadata': {},
    'summary': {},
    'transactions': []
  }

  for index, text in enumerate(STATEMENT_LIST):
    if (actions.get(text)):
      key = text[:-1]
      if (actions[text] is get_next):
        parsed_statement['metadata'][key] = actions[text](index)
      elif (actions[text] is get_paid_in_and_out):
        parsed_statement['summary'][key] = actions[text](index)
    elif is_date_string(text):
      transaction = retrieve_transaction_details(index)
      parsed_statement['transactions'].append(transaction)

  return parsed_statement

