import os
import re

files = [
    'scripts/builders/update_app_01.py',
    'scripts/builders/update_app_02.py',
    'scripts/builders/update_app_03.py',
    'scripts/builders/update_app_04.py',
    'scripts/builders/update_app_05.py',
    'scripts/builders/update_app_06.py',
    'scripts/builders/update_app_07.py',
    'scripts/builders/update_app_08.py',
    'scripts/builders/update_app_m2_01.py'
]

hint_btn = '''
                    <button class="btn btn-hint" onclick="alert('💡 힌트: ' + document.getElementById('error{qnum}').innerText)" style="margin-left:10px; background:rgba(16,185,129,0.2); border:1px solid rgba(16,185,129,0.5); color:#34D399;">💡 힌트</button>'''

new_else = '''}} else {{
                wrongCount++;
                if (wrongCount >= 3) {{
                    alert("🚨 3회 오답 패널티! 1구역으로 강제 이동됩니다.");
                    wrongCount = 0;
                    document.getElementById('ans1').value = '';
                    nextStage('panel_q{qnum}', 'panel_q1', 0);
                }} else {{
                    showError('panel_q{qnum}', 'error{qnum}');
                }}
            }}'''

for file in files:
    if not os.path.exists(file):
        continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add hint button (Regex is safe here since we just match the button tag)
    content = re.sub(r'(<button class="btn"[^>]*onclick="checkQ\{qnum\}\(\)"[^>]*>.*?</button>)', r'\1' + hint_btn, content)

    # Add wrongCount globally
    if 'let wrongCount = 0;' not in content:
        content = content.replace('function cleanString(str)', 'let wrongCount = 0;\n\n        function cleanString(str)')

    # Add wrongCount = 0 inside if ({ans_check})
    content = content.replace('if ({ans_check}) {{', 'if ({ans_check}) {{\n                wrongCount = 0;')

    # Replace else block
    # It usually is }} else {{\n                showError('panel_q{qnum}', 'error{qnum}');\n            }}
    # We can do this with regex matching }} else {{...showError...}}
    
    pattern = r'\}\}\s*else\s*\{\{\s*showError\(\'panel_q\{qnum\}\',\s*\'error\{qnum\}\'\);\s*\}\}'
    content = re.sub(pattern, new_else, content)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Updated exactly what was needed!")
