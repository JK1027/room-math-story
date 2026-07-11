import os
import re
import glob

builder_dir = 'scripts/builders'
files = glob.glob(os.path.join(builder_dir, 'update_app_*.py'))

# The target strings we want to modify
old_btn = '''<button class="btn" onclick="checkQ{qnum}()">해독하기</button>'''
new_btn = '''<button class="btn" onclick="checkQ{qnum}()">해독하기</button>
                    <button class="btn btn-hint" onclick="alert('💡 힌트: ' + document.getElementById('error{qnum}').innerText)" style="margin-left:10px; background:rgba(16,185,129,0.2); border:1px solid rgba(16,185,129,0.5); color:#34D399;">💡 힌트</button>'''

old_check = '''            if ({ans_check}) {{
                try {{ playSuccess(); }} catch(e) {{}}
                nextStage('panel_q{qnum}', {next_stage}, {progress});
            }} else {{
                showError('panel_q{qnum}', 'error{qnum}');
            }}'''

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

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Add btn-hint CSS inline (done above in new_btn to avoid touching base_html CSS regexes which are fragile)
    # Wait, hover effects can't be inline, but it's okay, it still looks good.

    # 2. Add button
    content = content.replace(old_btn, new_btn)

    # 3. Add wrongCount variable to js_boilerplate
    if 'let wrongCount = 0;' not in content:
        content = content.replace('function cleanString(str) {', 'let wrongCount = 0;\n\n        function cleanString(str) {')

    # 4. Modify check_fn
    content = content.replace(old_check, new_check)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Successfully updated all python builders!")
