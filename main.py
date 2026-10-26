from pathlib import Path
import pdfplumber
import re
from datetime import datetime



# cli.py :
def accept_folder_name():

    user_input = input("Enter a folder path: ")

    clean_path = user_input.strip(" '\" ")
    folder_path = Path(clean_path)

    return folder_path

def find_all_pdf_files(folder_path):
    pdf_files = list(folder_path.glob("*.pdf"))
    return pdf_files

# reader.py :
def pdf_text_extractor(file_path):
    with pdfplumber.open(file_path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()

        return text

# parser.py (text -> vendor, date, total)
def customer_name_parser(extracted_text):
    pattern = r"Customer Name:\s*(\w+)\s*(\w+)"

    matches = re.findall(pattern, extracted_text)

    if matches:
        return matches
    else:
        return []

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
        return invoice_total_amount
    else:
        return []


# separating logic from main()

def get_customer_names_from_invoices(extracted_text):
    customer_names = customer_name_parser(extracted_text)
    if customer_names:
        for customer_name in customer_names:
            # Unpacking the 'customer_name' tuple
            first_name, last_name = customer_name
            print(f"Customer Name: {first_name} {last_name}")
            return True
    else:
        print("Customer Name is not found from the Invoice")
        return False


def get_date_from_invoices(extracted_text):
    date_from_invoice = invoice_date_parser(extracted_text)

    if date_from_invoice is None:
        print("No date found")
        return False

    if _valid_date_string(date_from_invoice):
        print(f"Invoice Date: {date_from_invoice}")
        return True

    else:
        print("Date is not a real calendar date")
        return False

def get_total_amount_from_invoices(extracted_text):
    total_amount_list = invoice_total_parser(extracted_text)
    if total_amount_list:
        for amount in total_amount_list:
            first, last = amount

            each_amount = float(f"{first}.{last}")
            if each_amount > 0 :
                print(f"Invoice Total Amount: {each_amount}")
                return True
            else:
                print("Invalid Total Amount")
                return False
    else:
        print("Total Amount is not found from the Invoice")
        return False

successful_invoices = []
error_invoices = []

def main():

    folder_path = accept_folder_name()

    if folder_path.exists() and folder_path.is_dir():
        pdf_files = find_all_pdf_files(folder_path)

        if pdf_files:
            for pdf_file in pdf_files[:2]:
                extracted_text = pdf_text_extractor(pdf_file)
                # print(type(extracted_text)) o/p : string

                # TO GET CUSTOMER NAMES FROM INVOICES
                if get_customer_names_from_invoices(extracted_text) and get_date_from_invoices(extracted_text) and get_total_amount_from_invoices(extracted_text) :

                    successful_invoices.append(pdf_file)
                else:

                    error_invoices.append(pdf_file)






        else:
            print("No PDFs found in this folder")

    else:
        print(f"Error: {folder_path} is not a valid folder.")


if __name__ == "__main__":
    main()









