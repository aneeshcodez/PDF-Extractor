import re

from pdfminer.high_level import extract_pages,extract_text

text = extract_text("Script.pdf")
# print(text)

pattern = re.compile(r'Origa')

matches = pattern.finditer(text)
for match in matches:
    print(match)



