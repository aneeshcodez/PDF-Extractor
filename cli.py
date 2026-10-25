from pathlib import Path
import pdfplumber


# cli.py :
def accept_folder_name():

    user_input = input("Enter a folder path: ")

    clean_path = user_input.strip(" '\" ")
    folder_path = Path(clean_path)

    return folder_path

def find_all_pdf_files(folder_path):
    pdf_files = list(folder_path.glob("*.pdf"))
    return pdf_files

def main():

    folder_path = accept_folder_name()

    if folder_path.exists() and folder_path.is_dir():
        pdf_files = find_all_pdf_files(folder_path)

        if pdf_files:
            for pdf_file in pdf_files:
                print(pdf_file.name)
        else:
            print("No PDFs found in this folder")

    else:
        print(f"Error: {folder_path} is not a valid folder.")

# reader.py :





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