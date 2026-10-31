from parser import customer_name_parser
from parser import invoice_date_parser
from parser import invoice_total_parser
from parser import _valid_date_string


def get_customer_names_from_invoices(extracted_text):

    actual_customer_name = customer_name_parser(extracted_text)
    if actual_customer_name:
        return actual_customer_name
    else:
        return None



def get_date_from_invoices(extracted_text):
    date_from_invoice = invoice_date_parser(extracted_text)

    if date_from_invoice is None:
        return None

    if _valid_date_string(date_from_invoice):
        return date_from_invoice

    else:
        return None

def get_total_amount_from_invoices(extracted_text):
    amount = invoice_total_parser(extracted_text)

    if amount is not None and amount > 0 :
        return amount
    else:
        return None
