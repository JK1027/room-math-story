import os
import re
import json

current_dir = os.path.dirname(os.path.abspath(__file__)) # scripts/utils
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
mapping_json = r"C:\Users\user\.gemini\antigravity-ide\brain\834b5221-e11b-42d7-ae5c-626244470f54\scratch\mc_mapping.json"

with open(mapping_json, "r", encoding="utf-8") as f:
    mapping = json.load(f)

# Translate update_app_*.py names to output app_*.html names
def get_html_name(builder_name):
    # e.g., update_app_01.py -> app_m1_01_escape_room.html
    # update_app_m2_01.py -> app_m2_01_escape_room.html
    # update_app_m3_01.py -> app_m3_01_escape_room.html
    name_no_ext = builder_name.replace(".py", "")
    parts = name_no_ext.split("_")
    if len(parts) == 3: # update_app_01
        return f"app_m1_{parts[2]}_escape_room.html"
    elif len(parts) == 4: # update_app_m2_01 or m3_01
        return f"app_{parts[2]}_{parts[3]}_escape_room.html"
    return None

print(f"Starting post-processing for HTML multiple choice conversion...")

mc_css = """
        .radio-label {
            display: block;
            margin-bottom: 0.8rem;
            font-size: 1.1rem;
            cursor: pointer;
            text-align: left;
            padding: 0.5rem 1rem;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.1);
            transition: all 0.2s ease;
        }
        .radio-label:hover {
            background: rgba(0, 240, 255, 0.1);
            border-color: rgba(0, 240, 255, 0.3);
        }
        input[type="radio"] {
            margin-right: 0.8rem;
            transform: scale(1.2);
            cursor: pointer;
        }
"""

for builder_name, conversions in mapping.items():
    if not conversions:
        continue
        
    html_name = get_html_name(builder_name)
    if not html_name:
        continue
        
    html_path = os.path.join(apps_dir, html_name)
    if not os.path.exists(html_path):
        print(f"  HTML not found: {html_name}")
        continue
        
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    # We should ignore files that already have the CSS injected or check if we need to add it
    if ".radio-label" not in html_content:
        # Inject CSS before </style>
        # Handles both normal and minified css closing
        html_content = html_content.replace("</style>", f"{mc_css}</style>", 1)
        
    modified = False
    for conv in conversions:
        qnum = conv["qnum"]
        options = conv["options"]
        
        # 1. Replace the input group markup
        # Find the input group containing target input id ans{qnum}
        # Format might be slightly minified or spaced, so we use regex
        input_group_pattern = re.compile(
            r'<div class=["\']input-group["\']>\s*<input[^>]*id=["\']ans' + str(qnum) + r'["\'][^>]*>\s*</div>',
            re.DOTALL
        )
        
        # Construct options HTML
        options_html = ""
        for opt in options:
            options_html += f'''
                    <label class="radio-label">
                        <input type="radio" name="ans_group{qnum}" value="{opt}"> {opt}
                    </label>'''
                    
        mc_group_html = f'''
                    <div class="options-group" id="ans{qnum}_group" style="margin-top: 1.5rem; display: flex; flex-direction: column; gap: 0.5rem;">
                        {options_html}
                    </div>'''
                    
        # Apply replacement
        if input_group_pattern.search(html_content):
            html_content = input_group_pattern.sub(mc_group_html, html_content)
            modified = True
            
        # 2. Replace the answer fetch logic in javascript
        # Target: const ans = cleanString(document.getElementById('ans{qnum}').value);
        # (with or without semicolons, spaces, quotes)
        js_ans_pattern = re.compile(
            r'const\s+ans\s*=\s*cleanString\(document\.getElementById\(["\']ans' + str(qnum) + r'["\']\)\.value\);?',
            re.DOTALL
        )
        
        js_ans_replacement = f'''const checkedOpt = document.querySelector('input[name="ans_group{qnum}"]:checked'); const ans = checkedOpt ? checkedOpt.value : "";'''
        
        if js_ans_pattern.search(html_content):
            html_content = js_ans_pattern.sub(js_ans_replacement, html_content)
            modified = True
            
        # 3. Replace the reset logic in javascript (when 3 wrong answers reset to zone start)
        # Target: document.getElementById('ans{qnum}').value = '';
        js_reset_pattern = re.compile(
            r'document\.getElementById\(["\']ans' + str(qnum) + r'["\']\)\.value\s*=\s*["\']["\'];?',
            re.DOTALL
        )
        
        js_reset_replacement = f'''document.querySelectorAll('input[name="ans_group{qnum}"]').forEach(el => el.checked = false);'''
        
        if js_reset_pattern.search(html_content):
            html_content = js_reset_pattern.sub(js_reset_replacement, html_content)
            modified = True
            
    if modified:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Successfully processed HTML for Multiple Choice: {html_name}")
    else:
        print(f"No changes required for: {html_name}")

print("Post-processing complete.")
