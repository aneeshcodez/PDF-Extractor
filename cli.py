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
        return "Customer Name is empty"

def invoice_date_parser(extracted_text):
    pattern = r"\d{4}-\d{2}-\d{2}"

    date_list = re.findall(pattern,extracted_text)
    for date in date_list:
        if _valid_date_string(date):
            return date
        else:
            return "Date is not a real calendar date"



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
            first,last = amount
            if int(first) > 0 :
                return invoice_total_amount
            else:
                return "Invalid Invoice Amount"
    else:
        return "Total is not present in the Invoice"




def main():

    folder_path = accept_folder_name()

    if folder_path.exists() and folder_path.is_dir():
        pdf_files = find_all_pdf_files(folder_path)

        if pdf_files:
            for pdf_file in pdf_files[:2]:
                extracted_text = pdf_text_extractor(pdf_file)
                # print(type(extracted_text)) o/p : string

                # TO GET CUSTOMER NAMES FROM INVOICES
                customer_names = customer_name_parser(extracted_text)

                for customer_name in customer_names:
                    # Unpacking the 'customer_name' tuple
                    first_name, last_name = customer_name
                    print(f"Customer Name: {first_name} {last_name}")

                # TO GET DATE FROM THE INVOICES
                date = invoice_date_parser(extracted_text)
                print(f"Invoice Date: {date}")

                # TO GET THE TOTAL AMOUNT FROM INVOICES
                total_amount_list = invoice_total_parser(extracted_text)
                for amount in total_amount_list:
                    first,last = amount
                    print(f"Invoice Total Amount: {first}.{last}")



        else:
            print("No PDFs found in this folder")

    else:
        print(f"Error: {folder_path} is not a valid folder.")


if __name__ == "__main__":
    main()







'''
Read text from one PDF



Open a PDF.

Extract its text.

Check whether any text was extracted.



New concept: pdfplumber. Test this with just one invoice before processing multiple files.

1.First functions then Exceptional handling for the above code 

'''