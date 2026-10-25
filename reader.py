import pdfplumber

with pdfplumber.open("/Users/aneesh/Desktop/Sample Invoices/invoice_10255.pdf") as pdf:
    page = pdf.pages[0]
    text = page.extract_text()

    print(text)





'''
Read text from one PDF



Open a PDF.

Extract its text.

Check whether any text was extracted.



New concept: pdfplumber. Test this with just one invoice before processing multiple files.
'''