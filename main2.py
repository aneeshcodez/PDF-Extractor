import csv
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


# validator.py: (These are Validating functions)

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

successful_invoices = []
error_invoices = []


def write_successful_invoices_csv():
    print("Writing to Successful CSV File")
    fieldnames = ["PDF NAME", "CUSTOMER NAME", "INVOICE DATE", "TOTAL AMOUNT"]

    with open("successful_invoices.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        # 1.writer.writerows(list) writes the dictionaries as rows, matching their keys to the specified column names.
        # 2.But If you have a list of dictionaries, you need to loop through the list to access each dictionary's keys.
        for successful_invoice in successful_invoices:
            writer.writerow(successful_invoice)

def write_error_invoices_csv():
    print("Writing to Error CSV File")
    fieldnames = ["PDF NAME", "REASONS"]

    with open("error_invoices.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for error_invoice in error_invoices:
            writer.writerow(error_invoice)






def main():

    folder_path = accept_folder_name()

    if folder_path.exists() and folder_path.is_dir():
        pdf_files = find_all_pdf_files(folder_path)

        if pdf_files:
            for pdf_file in pdf_files[:2]:
                extracted_text = pdf_text_extractor(pdf_file)

                # Extract each field
                customer_name = get_customer_names_from_invoices(extracted_text)
                invoice_date = get_date_from_invoices(extracted_text)
                total_amount = get_total_amount_from_invoices(extracted_text)

                # Determines whether each invoice succeeded or failed.
                if (customer_name is not None and invoice_date is not None and total_amount is not None):
                    successful_invoices.append(
                        {
                            "PDF NAME" : pdf_file.name,
                            "CUSTOMER NAME" : customer_name,
                            "INVOICE DATE" : invoice_date,
                            "TOTAL AMOUNT" : total_amount
                        }

                    )

                else:
                    failure_reasons = []
                    if customer_name is None:
                        reason_1 = "customer name is not present in the Invoice"
                        failure_reasons.append(reason_1)
                    if invoice_date is None:
                        reason_2 = "Invoice Date is not present or Invalid Date"
                        failure_reasons.append(reason_2)
                    if total_amount is None:
                        reason_3 = "Total Amount is not present or Invalid Total Amount"
                        failure_reasons.append(reason_3)

                    all_failure_reasons = ";".join(failure_reasons)

                    error_invoices.append(
                        {
                            "PDF NAME": pdf_file.name,
                            "REASONS" : all_failure_reasons
                        }
                    )







        else:
            print("No PDFs found in this folder")

    else:
        print(f"Error: {folder_path} is not a valid folder.")

    write_successful_invoices_csv()

    write_error_invoices_csv()

    for successful_invoice in successful_invoices:
        print("printing from successful_invoices ")
        print(successful_invoice)

    for error_invoice in error_invoices:
        print(error_invoice)



if __name__ == "__main__":
    main()

'''
1.Get perfect code from AI TILL extracted values & validation 
2.Ask AI what mistake I was doing from the beginning itself AND Actually learn the pattern of 
how this should been done ,know its name in programming(like robust,encapsulation) and understand 
the WHY (like eg: For changing code later on)
3.After that start coding on your own from : Making a Dict and using that Dict to write to CSV Files
' # append_to_successful_invoices_list(pdf_file) # because filename is required '

IYW : We will go one by one , so first for Customer name , these are the changes I made in my code My code :

 


'''









