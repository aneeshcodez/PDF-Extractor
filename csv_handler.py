import csv

def write_successful_invoices_csv(successful_invoices):
    print("Writing to Successful CSV File")
    fieldnames = ["PDF NAME", "CUSTOMER NAME", "INVOICE DATE", "TOTAL AMOUNT"]

    with open("successful_invoices.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        # 1.writer.writerows(list) writes the dictionaries as rows, matching their keys to the specified column names.
        # 2.But If you have a list of dictionaries, you need to loop through the list to access each dictionary's keys.
        for successful_invoice in successful_invoices:
            writer.writerow(successful_invoice)

def write_error_invoices_csv(error_invoices):
    print("Writing to Error CSV File")
    fieldnames = ["PDF NAME", "REASONS"]

    with open("error_invoices.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for error_invoice in error_invoices:
            writer.writerow(error_invoice)