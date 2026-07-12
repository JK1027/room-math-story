import os
import re
import glob

builder_dir = 'scripts/builders'
files = glob.glob(os.path.join(builder_dir, 'update_app_*.py'))

new_check = '''            if ({ans_check}) {{
                try {{ playSuccess(); }} catch(e) {{}}
                wrongCount = 0;
                nextStage('panel_q{qnum}', {next_stage}, {progress});
            }} else {{
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

hint_btn = '''
                    <button class="btn btn-hint" onclick="alert('💡 힌트: ' + document.getElementById('error{qnum}').innerText)" style="margin-left:10px; background:rgba(16,185,129,0.2); border:1px solid rgba(16,185,129,0.5); color:#34D399;">💡 힌트</button>'''

count = 0
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. Add btn-hint button
    # Find button with onclick="checkQ{qnum}()"
    # Wait, some might have other styles or class names.
    content = re.sub(r'(<button[^>]*onclick="checkQ\{qnum\}\(\)"[^>]*>.*?</button>)', r'\1' + hint_btn, content)

    # 2. Add wrongCount variable to js_boilerplate
    if 'let wrongCount = 0;' not in content:
        content = re.sub(r'(function cleanString\()', r'let wrongCount = 0;\n\n        \1', content)

    # 3. Modify check_fn
    # We look for the exact structure of the else block.
    # The old structure might be the original one or already modified by v1 script.
    # Let's replace the original one if it exists.
    old_check_pattern = r'if \(\{ans_check\}\) \{\s*try \{ playSuccess\(\); \} catch\(e\) \{\}\s*nextStage\(\'panel_q\{qnum\}\', \{next_stage\}, \{progress\}\);\s*\} else \{\s*showError\(\'panel_q\{qnum\}\', \'error\{qnum\}\'\);\s*\}'
    
    if re.search(old_check_pattern, content):
        content = re.sub(old_check_pattern, new_check.strip(), content)

    if content != original:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        
print(f"Successfully updated {count} python builders with regex!")
