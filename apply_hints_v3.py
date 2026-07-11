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

for file in files:
    if not os.path.exists(file):
        continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add Hint Button
    # We find <button class="btn"[^>]*>.*?</button> inside the question-box block and append hint_btn.
    # Note: be careful not to replace multiple buttons. We just replace the button that has checkQ in its onclick.
    content = re.sub(r'(<button class="btn"[^>]*onclick="checkQ\{qnum\}\(\)"[^>]*>.*?</button>)', r'\1' + hint_btn, content)

    # 2. Add wrongCount = 0
    if 'let wrongCount = 0;' not in content:
        # insert before function cleanString
        content = re.sub(r'(function cleanString\()', r'let wrongCount = 0;\n\n        \1', content)

    # 3. Add wrongCount = 0 inside if (ans_check)
    content = re.sub(r'(if \(\{ans_check\}\) \{\s*)', r'\1wrongCount = 0;\n                ', content)

    # 4. Modify else block
    old_else = r'\} else \{\s*showError\(\'panel_q\{qnum\}\',\s*\'error\{qnum\}\'\);\s*\}'
    new_else = r'''} else {
                wrongCount++;
                if (wrongCount >= 3) {
                    alert("🚨 3회 오답 패널티! 1구역으로 강제 이동됩니다.");
                    wrongCount = 0;
                    document.getElementById('ans1').value = '';
                    nextStage('panel_q{qnum}', 'panel_q1', 0);
                } else {
                    showError('panel_q{qnum}', 'error{qnum}');
                }
            }'''
    content = re.sub(old_else, new_else, content)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Updated the remaining 9 files!")
