import re
from datetime import datetime


def customer_name_parser(extracted_text):
    pattern = r"Customer Name:\s*(\w+)\s*(\w+)"

    customer_names = re.findall(pattern, extracted_text)

    if customer_names:
        for customer_name in customer_names:
            # Unpacking the 'customer_name' tuple
            first_name, last_name = customer_name
            actual_customer_name = first_name + " " + last_name
            return actual_customer_name
    else:
        return None

def invoice_date_parser(extracted_text):
    pattern = r"\d{4}-\d{2}-\d{2}"

    date_list = re.findall(pattern,extracted_text)
    if date_list:
        return date_list[0]
    else:
        return None


def _valid_date_string(date):
    date_format = "%Y-%m-%d"
    try:
        datetime.strptime(date,date_format)
        return True
    except ValueError:
        return False

def invoice_total_parser(extracted_text):
    pattern = r"Total:\s*\$(\d+)\.(\d+)"

    invoice_total_amount = re.findall(pattern,extracted_text)

    if invoice_total_amount:
        for amount in invoice_total_amount:
            first, last = amount

            each_amount = float(f"{first}.{last}")

            return each_amount

    else:
        return None