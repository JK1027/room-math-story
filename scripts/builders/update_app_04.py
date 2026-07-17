import re
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "app_m1_04_escape_room.html")

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# ----------------- 마크다운 대본집 파서 및 데이터 로드 -----------------
def load_storyboard(file_path):
    img_map = {}
    qs = []
    events = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\r\n', '\n')
        
    # 1. 이미지 매핑 파싱
    img_map_match = re.search(r'# \[이미지 매핑\]\n([\s\S]*?)(?:\n---|\n# \[|$)', content)
    if img_map_match:
        lines = img_map_match.group(1).strip().split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('-'):
                parts = line[1:].split(':')
                if len(parts) >= 2:
                    key = parts[0].strip()
                    val = parts[1].strip()
                    if key.isdigit():
                        img_map[int(key)] = val
                    else:
                        img_map[key] = val

    # 2. 문항 정의 파싱 (Split 기반으로 겹침 매칭 원천 방지)
    q_parts = content.split('## Q')
    for part in q_parts[1:]:
        part_lines = part.strip().split('\n')
        qnum_str = part_lines[0].strip()
        if not qnum_str.isdigit():
            continue
        qnum = int(qnum_str)
        
        q_data = {"qnum": qnum}
        story_started = False
        story_lines = []
        
        for line in part_lines[1:]:
            if story_started:
                # 다음 문항이나 구분선을 만나면 지문 수집 종료
                if line.strip().startswith('---') or line.strip().startswith('# ['):
                    break
                story_lines.append(line)
                continue
                
            line_str = line.strip()
            if line_str.startswith('- 제목:'):
                q_data["title"] = line_str.replace('- 제목:', '').strip()
            elif line_str.startswith('- 질문:'):
                q_data["qtext"] = line_str.replace('- 질문:', '').strip()
            elif line_str.startswith('- 힌트:'):
                q_data["hint"] = line_str.replace('- 힌트:', '').strip()
            elif line_str.startswith('- 정답 체크:'):
                q_data["ans_check"] = line_str.replace('- 정답 체크:', '').strip()
            elif line_str.startswith('- 플레이스홀더:'):
                q_data["placeholder"] = line_str.replace('- 플레이스홀더:', '').strip()
            elif line_str.startswith('- 에러 메시지:'):
                q_data["error"] = line_str.replace('- 에러 메시지:', '').strip()
            elif line_str.startswith('- extra_class:'):
                q_data["extra_class"] = line_str.replace('- extra_class:', '').strip()
            elif line_str.startswith('- 선택지:'):
                opts_str = line_str.replace('- 선택지:', '').strip()
                q_data["options"] = [opt.strip() for opt in opts_str.split(',') if opt.strip()]
            elif line_str.startswith('- 지문:'):
                story_started = True
                
        q_data["story"] = '\n'.join(story_lines).strip()
        qs.append(q_data)

    # 3. 이벤트 정의 파싱 (Split 기반으로 겹침 매칭 원천 방지)
    event_parts = content.split('## EVENT')
    for part in event_parts[1:]:
        part_lines = part.strip().split('\n')
        evnum_str = part_lines[0].strip()
        if not evnum_str.isdigit():
            continue
        evnum = int(evnum_str)
        
        ev_data = {}
        story_started = False
        story_lines = []
        
        for line in part_lines[1:]:
            if story_started:
                if line.strip().startswith('---') or line.strip().startswith('# ['):
                    break
                story_lines.append(line)
                continue
                
            line_str = line.strip()
            if line_str.startswith('- 제목:'):
                ev_data["title"] = line_str.replace('- 제목:', '').strip()
            elif line_str.startswith('- 버튼 텍스트:'):
                ev_data["btn_text"] = line_str.replace('- 버튼 텍스트:', '').strip()
            elif line_str.startswith('- 다음 스테이지:'):
                ev_data["next_stage"] = line_str.replace('- 다음 스테이지:', '').strip()
            elif line_str.startswith('- 달성도:'):
                ev_data["progress"] = int(line_str.replace('- 달성도:', '').strip())
            elif line_str.startswith('- 지문:'):
                story_started = True
                
        ev_data["story"] = '\n'.join(story_lines).strip()
        events[evnum] = ev_data

    return img_map, qs, events

# 캐릭터 정의 및 동적 바인딩
nereus = "<span style='color: #60a5fa; text-shadow: 0 0 5px #3b82f6;'>[네레우스]</span>"
clio = "<span style='color: #c084fc; text-shadow: 0 0 5px #a855f7;'>[클리오]</span>"
poseidon = "<span class='glitch-text' style='color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;'>[포세이돈-V]</span>"
trident = "<span class='glitch-text' style='color: #fb923c; font-weight: bold; text-shadow: 0 0 5px #f97316;'>[트라이던트]</span>"
dyn_captain = "<span class='dynamic-captain-name'>캡틴</span>"

storyboard_path = os.path.join(project_root, "data", "storyboards", "중1", "m1_04_storyboard.md")
img_map, qs, events = load_storyboard(storyboard_path)

# 지문 내 변수 치환 적용
for q in qs:
    q["story"] = q["story"].replace("{nereus}", nereus).replace("{clio}", clio).replace("{poseidon}", poseidon).replace("{trident}", trident).replace("{dyn_captain}", dyn_captain)

for evnum, ev in events.items():
    ev["story"] = ev["story"].replace("{nereus}", nereus).replace("{clio}", clio).replace("{poseidon}", poseidon).replace("{trident}", trident).replace("{dyn_captain}", dyn_captain)

def make_event_html(evnum, ev, img_filename):
    return f'''
        <!-- Event {evnum}: {ev['title']} -->
        <div id="panel_event{evnum}" class="glass-panel">
            <h2>[이벤트] {ev['title']} <span class="game-timer" style="float: right; color: #ef4444; font-family: 'Share Tech Mono', monospace; font-size: 1.2rem; text-shadow: 0 0 5px #ef4444;">40:00</span></h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m1_04_coordinates/{img_filename}" alt="Event" class="panel-image">
            <div class="story-box">
                <div class="story-text">
                    {ev['story']}
                </div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <div class="btn-group">
                <button class="btn" onclick="nextStage('panel_event{evnum}', '{ev['next_stage']}', {ev['progress']})">{ev['btn_text']}</button>
            </div>
        </div>
'''

event1_html = make_event_html(1, events[1], img_map['event1'])
event2_html = make_event_html(2, events[2], img_map['event2'])
event3_html = make_event_html(3, events[3], img_map['event3'])
event4_html = make_event_html(4, events[4], img_map['event4'])


panels_html = ""
for i, q in enumerate(qs):
    qnum = q['qnum']
    title = q['title']
    story = q['story']
    qtext = q['qtext']
    placeholder = q['placeholder']
    error = q['error']
    
    hint_btn_html = f'<button class="btn-hint" onclick="alert(\'💡 힌트: {q["hint"]}\')">💡 힌트</button>'
    qtext_hinted = qtext.replace('</strong>', f'</strong> {hint_btn_html}', 1)
    
    extra_class = q.get('extra_class', '')
    qbox_id = 'id="q10-main-box" style="display:none;"' if qnum == 10 else ''
    
    if "options" in q:
        options_html = ""
        for idx, opt in enumerate(q["options"]):
            options_html += f'''
                    <label class="radio-label" style="display: block; margin-bottom: 0.8rem; font-size: 1.1rem; cursor: pointer; text-align: left; padding: 0.5rem 1rem; background: rgba(255,255,255,0.05); border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">
                        <input type="radio" name="ans_group{qnum}" value="{opt}" style="margin-right: 0.8rem; transform: scale(1.2); cursor: pointer;"> {opt}
                    </label>'''
        input_html = f'''
                    <div class="options-group" id="ans{qnum}_group" style="margin-top: 1.5rem; display: flex; flex-direction: column; gap: 0.5rem;">
                        {options_html}
                    </div>'''
    else:
        input_html = f'''
                    <div class="input-group">
                        <input type="text" id="ans{qnum}" placeholder="{placeholder}">
                    </div>'''

    panel = f'''
        <!-- Q{qnum} -->
        <div id="panel_q{qnum}" class="glass-panel {extra_class}">
            <h2>제 {qnum}구역: {title} <span class="game-timer" style="float: right; color: #ef4444; font-family: \'Share Tech Mono\', monospace; font-size: 1.2rem; text-shadow: 0 0 5px #ef4444;">40:00</span></h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m1_04_coordinates/{img_map[qnum]}" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text">{story}</div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <div class="question-box" {qbox_id}>
                <div class="question-content">
                    {qtext_hinted}
                    {input_html}
                </div>
            </div>
            <div class="error-msg" id="error{qnum}">{error}</div>
            <div class="btn-group">
                <button class="btn" onclick="checkQ{qnum}()">{'잠항 시작' if qnum==1 else '다음으로' if qnum < 20 else '탈출하기'}</button>
            </div>
        </div>
'''
    panels_html += panel

# 이벤트 패널들 추가
panels_html += event1_html + event2_html + event3_html + event4_html

outro_html = f'''
        <!-- 아웃트로 -->
        <div id="outro" class="glass-panel">
            <h1>탈출 성공!</h1>
            <h2>아틀란티스의 보물</h2>
            <img src="https://jk1027.github.io/room-math-story/apps/assets/m1_04_coordinates/{img_map['outro']}" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">미션 결과를 연산 중입니다...</div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <button class="btn" style="margin-top: 2rem;" onclick="location.reload()">다시 도전하기</button>
        </div>
'''
panels_html += outro_html

js_checks = "let totalWrongCount = 0;\n"
for q in qs:
    qnum = q['qnum']
    ans_check = q.get('ans_check', 'false')
    next_stage = f"'panel_q{qnum+1}'" if qnum < 20 else "'outro'"
    if qnum == 5:
        next_stage = "'panel_event1'"
    elif qnum == 10:
        next_stage = "'panel_event2'"
    elif qnum == 15:
        next_stage = "'panel_event3'"
    elif qnum == 20:
        next_stage = "'panel_event4'"

    next_progress = qnum*5
    victory_call = 'try { playVictory(); } catch(e) {}' if qnum == 20 else 'try { playSuccess(); } catch(e) {}'
    
    if qnum <= 5:
        reset_qnum = 1
        reset_prog = 0
        zone_name = "1구역"
    elif qnum <= 10:
        reset_qnum = 6
        reset_prog = 25
        zone_name = "2구역"
    elif qnum <= 15:
        reset_qnum = 11
        reset_prog = 50
        zone_name = "3구역"
    else:
        reset_qnum = 16
        reset_prog = 75
        zone_name = "4구역"

    gas_end_call = ""
    if qnum == 20:
        gas_end_call = f'''
                // GAS 기록 종료 호출
                try {{
                    if (window.userRecordRow && typeof google !== 'undefined' && google.script && google.script.run) {{
                        google.script.run.recordEnd(window.userRecordRow, 'm1_04');
                    }}
                }} catch(e) {{
                    console.warn("구글 시트 종료 기록 실패:", e);
                }}
                
                // 멀티 엔딩 처리
                let outroDiv = document.getElementById("outro-dynamic-text");
                if (outroDiv) {{
                    let firstName = window.playerFirstName || "캡틴";
                    if (totalWrongCount < 5) {{
                        outroDiv.innerHTML = "패널에 숫자 '-4'를 입력하는 순간! 지잉- 하는 거대한 소리와 함께 고대 AI 포세이돈-V가 문을 활짝 열어줍니다.<br><br>{poseidon}: '훌륭하다. 수천 년 만에 아틀란티스의 지혜를 물려줄 진정한 후계자를 만났군.'<br><br>{nereus}: '" + firstName + " 캡틴! 완벽합니다! 금화와 지식이 쏟아집니다, 어서 챙겨서 부상합시다!'<br><br>여러분은 완벽한 수학적 통찰력으로 심해의 전설을 정복했습니다. <b>[칭호 획득: 심연의 좌표 마스터]</b> 미션 대성공!";
                    }} else {{
                        outroDiv.innerHTML = "패널에 숫자 '-4'를 입력하는 순간! 지잉- 하는 거친 마찰음과 함께 문이 간신히 열립니다.<br><br>{poseidon}: '오답이 너무 많지만... 끈기 하나는 인정해주마. 얼른 가져가라.'<br><br>{nereus}: '" + firstName + " 캡틴! 간신히 황금 문이 열렸습니다! 보물을 다 챙길 시간은 없습니다. 당장 부력 장치를 가동해야 합니다!'<br><br>여러분은 황급히 금화 몇 닢을 챙기고 해수면으로 솟구쳐 오릅니다. 상처투성이의 탈출이었지만 미션 성공!";
                    }}
                }}'''

    if "options" in q:
        get_ans_js = f'''
            const checkedOpt = document.querySelector('input[name="ans_group{qnum}"]:checked');
            const ans = checkedOpt ? checkedOpt.value : "";
        '''
    else:
        get_ans_js = f'''
            const ans = cleanString(document.getElementById('ans{qnum}').value).replace('(','').replace(')','');
        '''

    reset_target_q = next((item for item in qs if item["qnum"] == reset_qnum), None)
    if reset_target_q and "options" in reset_target_q:
        reset_js = f'''
                    document.querySelectorAll('input[name="ans_group{reset_qnum}"]').forEach(el => el.checked = false);
        '''
    else:
        reset_js = f'''
                    document.getElementById('ans{reset_qnum}').value = '';
        '''

    js = f'''
        // Q{qnum}
        function checkQ{qnum}() {{
            {get_ans_js}
            if ({ans_check}) {{
                wrongCount = 0;
                {victory_call} {gas_end_call}
                nextStage('panel_q{qnum}', {next_stage}, {next_progress});
            }} else {{
                wrongCount++;
                totalWrongCount++;
                timeLeft -= 60;
                if (timeLeft < 0) timeLeft = 0;
                updateTimerDisplay();
                triggerTimerWarning();
                if (wrongCount >= 3) {{
                    showGlitchOverlay();
                    alert("🚨 3회 오답 패널티! {zone_name} 처음으로 이동됩니다.");
                    wrongCount = 0;
                    {reset_js}
                    nextStage('panel_q{qnum}', 'panel_q{reset_qnum}', {reset_prog});
                }} else {{
                    showError('panel_q{qnum}', 'error{qnum}', wrongCount);
                }}
            }}
        }}
'''
    js_checks += js

glitch_css = '''
.glitch-text { animation: shake 0.5s infinite; }
@keyframes shake {
    0% { transform: translate(1px, 1px) rotate(0deg); }
    10% { transform: translate(-1px, -2px) rotate(-1deg); }
    20% { transform: translate(-3px, 0px) rotate(1deg); }
    30% { transform: translate(3px, 2px) rotate(0deg); }
    40% { transform: translate(1px, -1px) rotate(1deg); }
    50% { transform: translate(-1px, 2px) rotate(-1deg); }
    60% { transform: translate(-3px, 1px) rotate(0deg); }
    70% { transform: translate(3px, 1px) rotate(-1deg); }
    80% { transform: translate(-1px, -1px) rotate(1deg); }
    90% { transform: translate(1px, 2px) rotate(0deg); }
    100% { transform: translate(1px, -2px) rotate(-1deg); }
}
.glitch-bg { animation: bg-glitch 0.3s linear infinite; }
@keyframes bg-glitch {
    0% { box-shadow: inset 0 0 10px #ef4444; }
    50% { box-shadow: inset 0 0 50px #ef4444; border: 2px solid #ef4444; }
    100% { box-shadow: inset 0 0 10px #ef4444; }
}
.timer-warning {
    animation: blink-red 0.2s 5;
    font-size: 1.5rem !important;
}
@keyframes blink-red {
    0%, 100% { color: #ef4444; text-shadow: 0 0 15px #ef4444; }
    50% { color: #ffffff; text-shadow: none; }
}
.glitch-overlay-screen {
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background: rgba(239, 68, 68, 0.15);
    z-index: 99999;
    display: none;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    pointer-events: none;
    box-sizing: border-box;
    border: 10px solid #ef4444;
    animation: pulse-border 0.2s infinite;
}
.glitch-overlay-text {
    font-family: 'Share Tech Mono', monospace;
    font-size: 3rem;
    color: #ef4444;
    font-weight: bold;
    text-shadow: 0 0 20px #ef4444;
    animation: shake 0.1s infinite;
}
.glitch-overlay-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.5rem;
    color: #ffffff;
    margin-top: 1rem;
}
@keyframes pulse-border {
    0%, 100% { border-color: #ef4444; background: rgba(239, 68, 68, 0.15); }
    50% { border-color: #ffffff; background: rgba(239, 68, 68, 0.3); }
}
.typing-cursor {
    animation: cursor-blink 0.8s infinite;
    font-weight: bold;
    color: var(--accent);
    margin-left: 2px;
}
@keyframes cursor-blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}
.radio-msg {
    color: #60a5fa;
    font-size: 0.95rem;
    margin-top: 0.5rem;
    font-weight: bold;
    text-shadow: 0 0 5px #3b82f6;
    text-align: center;
    animation: blink 1.5s infinite;
}
</style>
'''

glitch_html_js = '''
<!-- V3.0 UI Additions -->
<div id="glitchOverlay" class="glitch-overlay-screen">
    <div class="glitch-overlay-text">🚨 SYSTEM EXPLOITED 🚨</div>
    <div class="glitch-overlay-sub">ACCESS DENIED - CODE ERROR</div>
</div>

<!-- Game Over Panel -->
<div id="gameover" class="glass-panel">
    <h1 style="color: #ef4444; text-shadow: 0 0 15px #ef4444;">미션 실패 (GAME OVER)</h1>
    <h2>산소 고갈!</h2>
    <img src="https://jk1027.github.io/room-math-story/apps/assets/m1_04_coordinates/outro.png" alt="Game Over" class="panel-image" style="filter: grayscale(1) sepia(1) hue-rotate(-50deg);">
    <div class="story-box">
        <div class="story-text" style="color: #ef4444;">
            [포세이돈-V]: "시간 초과다! 역시 이 아틀란티스의 지혜를 받아들일 준비가 안 되어 있군. 돌아가라!"<br><br>
            잠수정의 산소 공급 장치가 완전히 멈췄습니다. 아쉽게도 탈출 좌표를 연산하지 못해 모험은 여기까지입니다. 숨을 고르고 다시 도전하세요!
        </div>
    </div>
    <button class="btn" style="margin-top: 2rem; background: #ef4444; border-color: #ef4444;" onclick="location.reload()">처음부터 다시 시도하기</button>
</div>

<script>
function showGlitchOverlay() {
    const overlay = document.getElementById('glitchOverlay');
    if (overlay) {
        overlay.style.display = 'flex';
        setTimeout(() => overlay.style.display = 'none', 1500);
    }
}

// showError 함수 오버라이딩 (네레우스 오답 무전 대응)
function showError(panelId, errorId, wrongCount) {
    try { playError(); } catch(e) {} 
    triggerLockdownAlert();
    const panel = document.getElementById(panelId);
    const errMsg = document.getElementById(errorId);
    
    panel.classList.remove('shake');
    void panel.offsetWidth; 
    panel.classList.add('shake');
    
    errMsg.style.display = 'block';
    
    let radioDiv = panel.querySelector('.radio-msg');
    if (!radioDiv) {
        radioDiv = document.createElement('div');
        radioDiv.className = 'radio-msg';
        errMsg.parentNode.insertBefore(radioDiv, errMsg.nextSibling);
    }
    
    let firstName = window.playerFirstName || "캡틴";
    
    if (wrongCount === 1) {
        radioDiv.innerHTML = "📡 [네레우스]: '" + firstName + " 캡틴, 사소한 계산 실수일 겁니다. 다시 계산해주십시오!'";
    } else if (wrongCount === 2) {
        radioDiv.innerHTML = "📡 [네레우스]: '경고! 다음 오답은 페널티가 발생합니다! 신중하게 골라주세요!'";
    } else {
        radioDiv.innerHTML = "";
    }
    
    setTimeout(() => { 
        errMsg.style.display = 'none'; 
        if (radioDiv) radioDiv.innerHTML = "";
    }, 3500);
}
</script>
'''

timer_replacement = '''
        function startTimer() {
            if (timerId) return;
            updateTimerDisplay();
            timerId = setInterval(() => {
                timeLeft--;
                if (timeLeft <= 0) {
                    clearInterval(timerId);
                    updateTimerDisplay();
                    document.querySelectorAll('.glass-panel').forEach(p => p.classList.remove('active'));
                    const goPanel = document.getElementById('gameover');
                    if (goPanel) goPanel.classList.add('active');
                    else {
                        alert("⏰ 제한 시간 초과!");
                        location.reload();
                    }
                } else {
                    updateTimerDisplay();
                }
            }, 1000);
        }
'''

def replace_between(text, start_str, end_str, replacement):
    start_idx = text.find(start_str)
    if start_idx == -1:
        print(f"Warning: Start marker '{start_str}' not found!")
        return text
    end_idx = text.find(end_str, start_idx + len(start_str))
    if end_idx == -1:
        print(f"Warning: End marker '{end_str}' not found after start marker!")
        return text
    return text[:start_idx] + replacement + text[end_idx:]

# 1. 패널 HTML 치환
new_content = replace_between(content, '<!-- Q1 -->', '<script>', '<!-- Q1 -->\n' + panels_html + '\n    </div>\n    ')

# 2. JS 치환 (오차 없는 완벽한 문자열 구분선 치환 적용)
start_marker = "// Q1"
end_marker = "window.onload = () => {"
# 들여쓰기 공백을 포함해 검색
end_idx_raw = new_content.find(end_marker)
if end_idx_raw != -1:
    start_search = end_idx_raw
    while start_search > 0 and new_content[start_search - 1] in [' ', '\t']:
        start_search -= 1
    end_marker_with_indent = new_content[start_search:end_idx_raw + len(end_marker)]
else:
    end_marker_with_indent = end_marker

# replacement 끝에 end_marker_with_indent 를 덧붙이지 않음 (원천적인 중복 정의 해결)
new_content = replace_between(new_content, start_marker, end_marker_with_indent, start_marker + '\n' + js_checks + '\n\n        ')

# 3. CSS 주입
if ".glitch-text" not in new_content:
    new_content = new_content.replace('</style>', glitch_css)

# 4. GameOver HTML 주입
if "glitchOverlay" not in new_content:
    new_content = new_content.replace('</body>', glitch_html_js + '\n</body>')

# 5. 타이머 교체
timer_pattern = r'function startTimer\(\) \{[\s\S]*?updateTimerDisplay\(\);\s*\}\s*,\s*1000\);\s*\}'
new_content = re.sub(timer_pattern, timer_replacement.strip(), new_content)

# 6. 동적 이름 치환 JS 주입 (tryStartGame) - 복성 예외 처리 로직 추가 (f-string이 아님에 유의)
name_injection_pattern = r'(const sid = document\.getElementById\(\'studentId\'\);[\s\S]*?const sname = document\.getElementById\(\'studentName\'\);[\s\S]*?return;\s*\})'
double_name_js = r'''\1

            // 이름 동적 개인화 처리 (복성 예외 처리 반영 및 전역 변수 바인딩)
            try {
                const doubleLastNames = ["제갈", "황보", "사공", "남궁", "서문", "독고", "선우"];
                let rawName = sname.value.trim();
                let firstName = rawName;
                if (rawName.length > 2) {
                    let prefix2 = rawName.substring(0, 2);
                    if (doubleLastNames.includes(prefix2)) {
                        firstName = rawName.substring(2);
                    } else {
                        firstName = rawName.substring(1);
                    }
                }
                window.playerFirstName = firstName;
                document.querySelectorAll(".dynamic-captain-name").forEach(el => {
                    let originalRole = el.getAttribute("data-original-role") || el.innerText;
                    if (!el.hasAttribute("data-original-role")) {
                        el.setAttribute("data-original-role", originalRole);
                    }
                    el.innerHTML = firstName + " " + originalRole;
                });
            } catch(e) { console.error("이름 파싱 에러:", e); }'''

if "window.playerFirstName" not in new_content:
    new_content = re.sub(name_injection_pattern, double_name_js, new_content)

# 7. 타이머 중복 중괄호 찌꺼기 완전 소거 (빌더 레벨 멱등성 보장 조치)
if "function nextStage" in new_content:
    timer_body_end = new_content.find("function startTimer() {")
    if timer_body_end != -1:
        normal_end = new_content.find("}, 1000);\n        }", timer_body_end)
        if normal_end != -1:
            normal_end_pos = normal_end + len("}, 1000);\n        }")
            next_stage_pos = new_content.find("function nextStage", normal_end_pos)
            if next_stage_pos != -1:
                new_content = new_content[:normal_end_pos] + "\n\n        " + new_content[next_stage_pos:]

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Updated successfully.")
