from pathlib import Path

def accept_folder_name():

    user_input = input("Enter a folder path: ")

    clean_path = user_input.strip(" '\" ")
    folder_path = Path(clean_path)

    return folder_path



def find_all_pdf_files(folder_path):
    if folder_path.exists():
        pdf_files = list(folder_path.glob("*.pdf"))
        if pdf_files:
            for f in pdf_files:
                print(f.name)
        else:
            print("No PDFs found in this folder")
    else:
        print(f"Error: The path '{folder_path}' does not exist.")


accept_folder_name()