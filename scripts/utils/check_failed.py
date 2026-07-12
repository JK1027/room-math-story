import glob
files = glob.glob('scripts/builders/update_app_*.py')
failed = []
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        if 'wrongCount++;' not in content:
            failed.append(f)
print("Files missing wrongCount: ", failed)
