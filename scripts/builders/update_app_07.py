import re

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m1_07_escape_room.html")

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

qs = []

# Generate panels
panels_html = ""
for i, q in enumerate(qs):
    qnum = q['qnum']
    title = q['title']
    story = q['story']
    qtext = q['qtext']
    placeholder = q['placeholder']
    error = q['error']
    
    prev_stage = f"'panel_q{qnum-1}'" if qnum > 1 else "'intro'"
    prev_progress = (qnum-1)*5
    next_stage = f"'panel_q{qnum+1}'" if qnum < 20 else "'outro'"
    next_progress = qnum*5
    
    panel = f'''
        <!-- Q{qnum} -->
        <div id="panel_q{qnum}" class="glass-panel">
            <h2>제 {qnum}구역: {title}</h2>
            <img src="assets/m1_07_solid_geometry/q{qnum}.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text">{story}</div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <div class="question-box">
                <div class="question-content">
                    {qtext}
                    <div class="input-group">
                        <input type="text" id="ans{qnum}" placeholder="{placeholder}">
                    </div>
                </div>
            </div>
            <div class="error-msg" id="error{qnum}">{error}</div>
            <div class="btn-group">
                <button class="btn" onclick="checkQ{qnum}()">{'잠항 시작' if qnum==1 and "update_app_06.py"=="update_app_04.py" else '미궁 진입' if qnum==1 and "update_app_06.py"=="update_app_06.py" else '시스템 복구 시작' if qnum==1 else '다음으로' if qnum < 20 else '탈출하기'}</button>
                    <button class="btn btn-hint" onclick="alert('💡 힌트: ' + document.getElementById('error{qnum}').innerText)" style="margin-left:10px; background:rgba(16,185,129,0.2); border:1px solid rgba(16,185,129,0.5); color:#34D399;">💡 힌트</button>
                    <button class="btn btn-hint" onclick="alert('💡 힌트: ' + document.getElementById('error{qnum}').innerText)" style="margin-left:10px; background:rgba(16,185,129,0.2); border:1px solid rgba(16,185,129,0.5); color:#34D399;">💡 힌트</button>
            </div>
        </div>
'''
    panels_html += panel

# Outro panel
outro_html = '''
        <!-- 아웃트로 -->
        <div id="outro" class="glass-panel">
            <h1>탈출 성공!</h1>
            <h2>태양 신전의 거울 미궁</h2>
            <img src="assets/m1_07_solid_geometry/outro.png" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text">여러분들이 땀을 흘리며 석문에 정답을 입력하고 다이얼을 돌리는 순간! 
                천장에서 쏟아지던 뜨겁고 살인적인 빛줄기가 마지막 거울에 반사되어 지하에 있는 깊은 냉각 수조의 중심부로 정확히 꽂힙니다. 
                쉭-! 하는 굉음과 함께 하얀 수증기가 신전을 가득 채우더니, 이내 굳게 닫혀 있던 탈출용 거대 돌벽이 스르륵 내려앉습니다. 
                눈을 뜰 수 없이 밝은 사막의 태양과 시원한 모래바람이 밀려옵니다. 거울 미궁 탈출에 성공했습니다!</div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <button class="btn" style="margin-top: 2rem;" onclick="location.reload()">다시 도전하기</button>
        </div>
'''
panels_html += outro_html

# Generate JS checks
js_checks = ""
for q in qs:
    qnum = q['qnum']
    ans_check = q['ans_check']
    next_stage = f"'panel_q{qnum+1}'" if qnum < 20 else "'outro'"
    next_progress = qnum*5
    victory_call = 'playVictory();' if qnum == 20 else 'playSuccess();'
    
    js = f'''
        // Q{qnum}
        function checkQ{qnum}() {{
            const ans = cleanString(document.getElementById('ans{qnum}').value).replace(/\\s+/g, '');
            if ({ans_check}) {{
                wrongCount = 0;
                {victory_call} 
                nextStage('panel_q{qnum}', {next_stage}, {next_progress});
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
            }}
        }}
'''
    js_checks += js


# We use regex to replace everything between the start of the first panel and <script> tag
import re
new_content = re.sub(r'<!-- Q1.*?<script>', lambda m: '<!-- Q1 -->\n' + panels_html + '\n        <script>', content, flags=re.DOTALL)

# And for JS:
new_content = re.sub(r'// Q1[\s\S]*?window\.onload = \(\) => \{', lambda m: '// Q1\n' + js_checks + '\n        window.onload = () => {', new_content)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("App 06 updated successfully with regex.")
