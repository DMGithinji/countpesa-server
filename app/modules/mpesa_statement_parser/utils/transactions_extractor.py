from .date_utils import convert_to_datetime, convert_to_number, is_date_string
from .metadata_extractor import get_transaction_metadata


def get_transactions(STATEMENT_LIST):
    """
    Extracts all transactions from a statement downloaded from MPESA APP

    Parameters:
    STATEMENT_LIST (list of str): A list of string values extracted from the statement
    """
    STATEMENT_DICT = {index: value for index, value in enumerate(STATEMENT_LIST)}

    def retrieve_transaction_details(transaction_date_index):
        """returns a single transaction dict given the index of the completion status"""
        transaction_description = ""

        pointer = transaction_date_index + 1
        while STATEMENT_DICT.get(pointer) and STATEMENT_DICT[pointer].lower() != "completed":
            transaction_description += f"{STATEMENT_DICT[pointer]} "
            pointer += 1

        metadata = get_transaction_metadata(transaction_description.strip())
        return {
            "code": STATEMENT_DICT[transaction_date_index - 1],
            "date": convert_to_datetime(STATEMENT_DICT[transaction_date_index]),
            "description": transaction_description.strip(),
            "status": STATEMENT_DICT[pointer],
            "amount": convert_to_number(STATEMENT_DICT[pointer + 1]),
            "balance": convert_to_number(STATEMENT_DICT[pointer + 2]),
            "account": metadata["account"],
            "type": metadata["type"],
            "category": metadata["category"],
        }

    parsed_statement = {"transactions": []}

    for index, text in enumerate(STATEMENT_LIST):
        if is_date_string(text):
            transaction = retrieve_transaction_details(index)
            parsed_statement["transactions"].append(transaction)

    return parsed_statement
