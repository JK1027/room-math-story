import os
import re
import json
import shutil

# Paths
current_dir = os.path.dirname(os.path.abspath(__file__)) # scripts/utils
project_root = os.path.dirname(os.path.dirname(current_dir))
builders_dir = os.path.join(project_root, "scripts", "builders")
mapping_json = r"C:\Users\user\.gemini\antigravity-ide\brain\834b5221-e11b-42d7-ae5c-626244470f54\scratch\mc_mapping.json"

# Load mapping data
with open(mapping_json, "r", encoding="utf-8") as f:
    mapping = json.load(f)

print(f"Loaded multiple choice mapping for {len(mapping)} files.")

def inject_options(file_path, conversions):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    modified = False
    for conv in conversions:
        qnum = conv["qnum"]
        options = conv["options"]
        
        # We need to find the dict for this qnum and inject "options": [...]
        # Let's search for "qnum": qnum
        # Match "qnum": N, including the trailing comma and optional spaces
        qnum_pat = re.compile(r'(["\']qnum["\']\s*:\s*' + str(qnum) + r'\s*,)')
        
        match = qnum_pat.search(content)
        if not match:
            print(f"  Warning: qnum {qnum} not found in {os.path.basename(file_path)}")
            continue
            
        # Find the boundaries of the dictionary containing this qnum
        start_idx = match.start()
        
        # Search backward for the opening '{' of this dictionary
        open_brace_idx = -1
        brace_count = 0
        for i in range(start_idx, -1, -1):
            if content[i] == '}':
                brace_count -= 1
            elif content[i] == '{':
                brace_count += 1
                if brace_count == 1:
                    open_brace_idx = i
                    break
                    
        if open_brace_idx == -1:
            print(f"  Warning: Could not find opening brace for qnum {qnum} in {os.path.basename(file_path)}")
            continue
            
        # Search forward for the closing '}' of this dictionary
        close_brace_idx = -1
        brace_count = 0
        for i in range(open_brace_idx, len(content)):
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    close_brace_idx = i
                    break
                    
        if close_brace_idx == -1:
            print(f"  Warning: Could not find closing brace for qnum {qnum} in {os.path.basename(file_path)}")
            continue
            
        dict_text = content[open_brace_idx : close_brace_idx + 1]
        
        # Check if options already exist in this dictionary to avoid duplicate injection
        if "options" in dict_text:
            print(f"  Info: qnum {qnum} in {os.path.basename(file_path)} already has options. Skipping.")
            continue
            
        # Inject "options": [...] inside the brace
        # We can format it nicely: {"qnum": N, "options": [...], ...
        options_repr = json.dumps(options, ensure_ascii=False)
        
        # Replace the first occurrence of "qnum": N, with "qnum": N, "options": [...]
        # Using the matched text from qnum_pat (which contains the comma)
        matched_str = match.group(1)
        replacement_str = f'{matched_str} "options": {options_repr},'
        
        # Make the change in the dict_text
        new_dict_text = dict_text.replace(matched_str, replacement_str, 1)
        
        # Replace the dict_text in the overall content
        content = content[:open_brace_idx] + new_dict_text + content[close_brace_idx + 1:]
        modified = True
        print(f"  Injected options into qnum {qnum} in {os.path.basename(file_path)}")
        
    if modified:
        # Save a backup first
        backup_path = file_path + ".bak"
        shutil.copyfile(file_path, backup_path)
        
        # Write modified content
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully updated {os.path.basename(file_path)} (Backup saved to {os.path.basename(backup_path)})")
    else:
        print(f"No changes made to {os.path.basename(file_path)}")

# Iterate and apply conversions
for file_name, conversions in mapping.items():
    if not conversions:
        continue
    file_path = os.path.join(builders_dir, file_name)
    if os.path.exists(file_path):
        print(f"Processing {file_name}...")
        inject_options(file_path, conversions)
    else:
        print(f"File not found: {file_path}")
