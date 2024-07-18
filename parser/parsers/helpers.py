import re
from datetime import datetime

def is_date_string(text):
    pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
    return re.search(pattern, text)

def convert_to_number(number_str):
    number_str = number_str.replace(',', '')
    try:
        number_float = float(number_str)
    except ValueError:
        return None
    return round(number_float, 2)

def convert_to_datetime(date_string):
    date_format = '%Y-%m-%d %H:%M:%S'
    timestamp = datetime.strptime(date_string, date_format).timestamp()
    return int(timestamp)
