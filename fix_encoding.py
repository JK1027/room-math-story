import re

file_path = 'scripts/builders/update_app_07.py'
with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Remove all characters that are not ASCII or Korean
# Wait, let's just remove the specific \x80
content = content.replace('\x80', '')
content = content.replace('', '')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
