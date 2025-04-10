from .text_extractor import get_pdf_text
from .transactions_extractor import get_transactions


def get_parsed_statement(parsed_file, password):
    text_content = get_pdf_text(parsed_file, password)
    statement_list = text_content.split("\n")
    parsed_statement = get_transactions(statement_list)
    return parsed_statement
