import re

text = "Name: Ram"

pattern = r"Price:\s*\d+"

matches = re.findall(pattern, text)

print(matches)
