import os
import glob
import re

scripts = ['scripts/builders/update_app_04.py', 'scripts/builders/update_app_06.py', 'scripts/builders/update_app_07.py']

for script_path in scripts:
    with open(script_path, 'r', encoding='utf-8') as f:
        code = f.read()

    code = code.replace("45분", "40분")
    code = code.replace("60분", "40분")

    h2_pattern1 = r'<h2>제 \{qnum\}구역: \{title\}<\/h2>'
    h2_pattern2 = r'<h2>제\{qnum\}구역: \{title\}<\/h2>'
    
    timer_html = r' <span class="game-timer" style="float: right; color: #ef4444; font-family: \'Share Tech Mono\', monospace; font-size: 1.2rem; text-shadow: 0 0 5px #ef4444;">40:00</span>'
    
    if "class=\"game-timer\"" not in code:
        code = re.sub(h2_pattern1, '<h2>제 {qnum}구역: {title}' + timer_html + '</h2>', code)
        code = re.sub(h2_pattern2, '<h2>제{qnum}구역: {title}' + timer_html + '</h2>', code)

    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(code)

print("Fixed 04, 06, 07 Python scripts.")
