from pathlib import Path
import pdfplumber
import re


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

    return matches

def main():

    folder_path = accept_folder_name()

    if folder_path.exists() and folder_path.is_dir():
        pdf_files = find_all_pdf_files(folder_path)

        if pdf_files:
            for pdf_file in pdf_files[:2]:
                extracted_text = pdf_text_extractor(pdf_file)
                # print(type(extracted_text)) o/p : string

                # To get customer Names from the PDFs
                customer_names = customer_name_parser(extracted_text)
                # print(customer_names)
                for customer_name in customer_names:
                    # Unpacking the 'customer_name' tuple
                    first_name, last_name = customer_name
                    print(f"{first_name} {last_name}")

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