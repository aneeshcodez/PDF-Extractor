from pathlib import Path
import pdfplumber
import re
from datetime import datetime


# cli.py
def accept_folder_name():
    user_input = input("Enter a folder path: ")
    clean_path = user_input.strip(" '\" ")
    folder_path = Path(clean_path)
    return folder_path


def find_all_pdf_files(folder_path):
    pdf_files = list(folder_path.glob("*.pdf"))
    return pdf_files


# reader.py
def pdf_text_extractor(file_path):
    with pdfplumber.open(file_path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
        return text


# parser.py (text -> customer name, date, total)
def customer_name_parser(extracted_text):
    pattern = r"Customer Name:\s*(\w+)\s*(\w+)"
    matches = re.findall(pattern, extracted_text)

    if matches:
        first_name, last_name = matches[0]
        return f"{first_name} {last_name}"
    else:
        return None


def invoice_date_parser(extracted_text):
    pattern = r"\d{4}-\d{2}-\d{2}"
    date_list = re.findall(pattern, extracted_text)

    if date_list:
        return date_list[0]
    else:
        return None


def _valid_date_string(date):
    date_format = "%Y-%m-%d"

    try:
        datetime.strptime(date, date_format)
        return True
    except ValueError:
        return False


def invoice_total_parser(extracted_text):
    pattern = r"Total:\s*\$(\d+)\.(\d+)"
    invoice_total_amount = re.findall(pattern, extracted_text)

    if invoice_total_amount:
        first, last = invoice_total_amount[0]
        return float(f"{first}.{last}")
    else:
        return None


# Validation functions
def get_customer_names_from_invoices(extracted_text):
    customer_name = customer_name_parser(extracted_text)

    if customer_name:
        return customer_name
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
    total_amount = invoice_total_parser(extracted_text)

    if total_amount is not None and total_amount > 0:
        return total_amount
    else:
        return None


successful_invoices = []
error_invoices = []


def main():
    folder_path = accept_folder_name()

    if folder_path.exists() and folder_path.is_dir():
        pdf_files = find_all_pdf_files(folder_path)

        if pdf_files:
            for pdf_file in pdf_files[:2]:
                extracted_text = pdf_text_extractor(pdf_file)

                # Extract and validate each field
                customer_name = get_customer_names_from_invoices(extracted_text)
                invoice_date = get_date_from_invoices(extracted_text)
                total_amount = get_total_amount_from_invoices(extracted_text)

                # Determine whether the invoice succeeded or failed
                if (
                    customer_name is not None
                    and invoice_date is not None
                    and total_amount is not None
                ):
                    successful_invoices.append(
                        (pdf_file, customer_name, invoice_date, total_amount)
                    )
                else:
                    error_invoices.append(pdf_file)

        else:
            print("No PDFs found in this folder")

    else:
        print(f"Error: {folder_path} is not a valid folder.")

    for successful_invoice in successful_invoices:
        print(successful_invoice)

    for error_invoice in error_invoices:
        print(error_invoice)


if __name__ == "__main__":
    main()