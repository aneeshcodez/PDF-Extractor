from cli import accept_folder_name, find_all_pdf_files
from reader import pdf_text_extractor
from validator import (
    get_customer_names_from_invoices,
    get_date_from_invoices,
    get_total_amount_from_invoices
)
from csv_handler import (
    write_successful_invoices_csv,
    write_error_invoices_csv
)
from summary import final_summary


successful_invoices = []
error_invoices = []


def main():
    folder_path = accept_folder_name()

    if folder_path.exists() and folder_path.is_dir():
        pdf_files = find_all_pdf_files(folder_path)

        if pdf_files:
            for pdf_file in pdf_files:
                extracted_text = pdf_text_extractor(pdf_file)

                # Extract each field
                customer_name = get_customer_names_from_invoices(extracted_text)
                invoice_date = get_date_from_invoices(extracted_text)
                total_amount = get_total_amount_from_invoices(extracted_text)

                # Determines whether each invoice succeeded or failed.
                if (customer_name is not None and invoice_date is not None and total_amount is not None):
                    successful_invoices.append(
                        {
                            "PDF NAME": pdf_file.name,
                            "CUSTOMER NAME": customer_name,
                            "INVOICE DATE": invoice_date,
                            "TOTAL AMOUNT": total_amount
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
                            "REASONS": all_failure_reasons
                        }
                    )

            write_successful_invoices_csv(successful_invoices)

            write_error_invoices_csv(error_invoices)

            final_summary(successful_invoices, error_invoices)
        else:
            print("No PDFs found in this folder")

    else:
        print(f"Error: {folder_path} is not a valid folder.")


if __name__ == "__main__":
    main()