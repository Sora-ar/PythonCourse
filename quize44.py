import re

pattern = r"\b\w{3}\b"
text = input("Enter text: ")
result = re.findall(pattern, text)
print(result)
