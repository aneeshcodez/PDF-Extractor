from pathlib import Path

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

if __name__ == "__main__":
    main()







'''
Find all PDF files in a folder : 

Accept a folder path from the user.

Find all PDF files inside it.

If there are no PDFs, display a message.

Keep it simple: use a folder path you specify in your project initially. Command-line arguments can come later.

1.First functions then Exceptional handling for the above code 

'''