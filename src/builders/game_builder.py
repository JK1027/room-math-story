import os
import re
from src.domain.models import Chapter
from src.builders.base import Builder
from scripts.config import paths

class GameBuilder(Builder):
    """
    [Game Builder 코어] chapterXX.md의 불변 도메인 모델을 읽어
    apps/ 하위의 뼈대 HTML 파일을 읽어 퀴즈 패널과 정답 판별 JS 로직을 
    동적으로 컴파일 덮어쓰는 통합 빌더입니다.
    """
    
    def replace_between(self, text: str, start_str: str, end_str: str, replacement: str) -> str:
        start_idx = text.find(start_str)
        if start_idx == -1:
            return text
        end_idx = text.find(end_str, start_idx + len(start_str))
        if end_idx == -1:
            return text
        return text[:start_idx] + replacement + text[end_idx:]

    def build(self, chapter: Chapter, grade_str: str, unit_code: str) -> bool:
        # 최종 산출물 폴더 (build/webapps) 및 원본 apps 폴더 설정
        output_dir = paths.ROOT_DIR / "build" / "webapps"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 뼈대가 되는 apps/app_{unit_code}_escape_room.html 파일 로드
        apps_dir = paths.APPS_DIR
        base_html_name = f"app_{unit_code}_escape_room.html"
        base_html_path = apps_dir / base_html_name
        
        if not base_html_path.exists():
            print(f"  [Error] Base game template not found: {base_html_path}", file=sys.stderr)
            return False
            
        with open(base_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 에셋 폴더명 찾기
        assets_folder = None
        apps_assets_root = apps_dir / "assets"
        if apps_assets_root.exists():
            for dname in os.listdir(apps_assets_root):
                if dname.startswith(unit_code) and os.path.isdir(apps_assets_root / dname):
                    assets_folder = dname
                    break
        if not assets_folder:
            assets_folder = unit_code

        # 지문 내 캐릭터 명 스타일 치환 설정
        hero_style = f"<span style='color: #60a5fa; text-shadow: 0 0 5px #3b82f6;'>[{chapter.hero}]</span>"
        helper_style = f"<span style='color: #c084fc; text-shadow: 0 0 5px #a855f7;'>[{chapter.helper}]</span>"
        villain_style = f"<span class='glitch-text' style='color: #ef4444; font-weight: bold; text-shadow: 0 0 5px #ef4444;'>[{chapter.villain}]</span>"
        dyn_captain_style = f"<span class='dynamic-captain-name'>{chapter.hero}</span>"

        def apply_character_styling(text_body: str) -> str:
            # 대본 속의 {hero}, {helper}, {villain} 등을 HTML 전용 컬러 스팬 태그로 교체
            text_body = text_body.replace("{hero}", hero_style)
            text_body = text_body.replace("{helper}", helper_style)
            text_body = text_body.replace("{villain}", villain_style)
            text_body = text_body.replace("{dyn_captain}", dyn_captain_style)
            # 호환성을 위해 그리스 신화 캐릭터 변수들도 유연 치환
            text_body = text_body.replace("{nereus}", helper_style)
            text_body = text_body.replace("{clio}", helper_style)
            text_body = text_body.replace("{poseidon}", villain_style)
            text_body = text_body.replace("{trident}", villain_style)
            return text_body

        # ─── 1. EVENT 패널 생성 ─────────────────────────────
        event_panels = []
        for idx, ev in enumerate(chapter.events, 1):
            styled_story = apply_character_styling(ev.story)
            img_url = f"https://jk1027.github.io/room-math-story/apps/assets/{assets_folder}/{ev.image}"
            
            ev_html = f'''
        <!-- Event {ev.evnum}: {ev.title} -->
        <div id="panel_event{ev.evnum}" class="glass-panel">
            <h2>[이벤트] {ev.title} <span class="game-timer" style="float: right; color: #ef4444; font-family: 'Share Tech Mono', monospace; font-size: 1.2rem; text-shadow: 0 0 5px #ef4444;">40:00</span></h2>
            <img src="{img_url}" alt="Event" class="panel-image">
            <div class="story-box">
                <div class="story-text">
                    {styled_story}
                </div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <div class="btn-group">
                <button class="btn" onclick="nextStage('panel_event{ev.evnum}', '{ev.next_stage}', {ev.progress})">{ev.btn_text}</button>
            </div>
        </div>
'''
            event_panels.append(ev_html)

        # ─── 2. QUESTION 패널 생성 ──────────────────────────
        question_panels = []
        js_checks = "let totalWrongCount = 0;\n"
        
        for idx, q in enumerate(chapter.questions, 1):
            styled_story = apply_character_styling(q.story)
            img_url = f"https://jk1027.github.io/room-math-story/apps/assets/{assets_folder}/{q.image}"
            
            hint_btn_html = f'<button class="btn-hint" onclick="alert(\'💡 힌트: {q.hint}\')">💡 힌트</button>'
            qtext_hinted = q.qtext.replace('</strong>', f'</strong> {hint_btn_html}', 1)
            
            qbox_id = 'id="q10-main-box" style="display:none;"' if q.qnum == 10 else ''
            
            # 주관식 vs 라디오 객관식 조립
            if q.choices:
                options_html = ""
                for opt in q.choices:
                    options_html += f'''
                    <label class="radio-label" style="display: block; margin-bottom: 0.8rem; font-size: 1.1rem; cursor: pointer; text-align: left; padding: 0.5rem 1rem; background: rgba(255,255,255,0.05); border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">
                        <input type="radio" name="ans_group{q.qnum}" value="{opt}" style="margin-right: 0.8rem; transform: scale(1.2); cursor: pointer;"> {opt}
                    </label>'''
                input_html = f'''
                    <div class="options-group" id="ans{q.qnum}_group" style="margin-top: 1.5rem; display: flex; flex-direction: column; gap: 0.5rem;">
                        {options_html}
                    </div>'''
            else:
                input_html = f'''
                    <div class="input-group">
                        <input type="text" id="ans{q.qnum}" placeholder="{q.placeholder}">
                    </div>'''
                    
            btn_txt = '잠항 시작' if q.qnum == 1 else '다음으로' if q.qnum < 20 else '탈출하기'
            extra_cls = q.extra_class if q.extra_class else ''
            
            panel = f'''
        <!-- Q{q.qnum} -->
        <div id="panel_q{q.qnum}" class="glass-panel {extra_cls}">
            <h2>제 {q.qnum}구역: {q.title} <span class="game-timer" style="float: right; color: #ef4444; font-family: 'Share Tech Mono', monospace; font-size: 1.2rem; text-shadow: 0 0 5px #ef4444;">40:00</span></h2>
            <img src="{img_url}" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text">{styled_story}</div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <div class="question-box" {qbox_id}>
                <div class="question-content">
                    {qtext_hinted}
                    {input_html}
                </div>
            </div>
            <div class="error-msg" id="error{q.qnum}">{q.error_message}</div>
            <div class="btn-group">
                <button class="btn" onclick="checkQ{q.qnum}()">{btn_txt}</button>
            </div>
        </div>
'''
            question_panels.append(panel)
            
            # 정답 판별 JS 조립
            next_stage = f"'panel_q{q.qnum+1}'" if q.qnum < 20 else "'outro'"
            if q.qnum == 5:
                next_stage = "'panel_event1'"
            elif q.qnum == 10:
                next_stage = "'panel_event2'"
            elif q.qnum == 15:
                next_stage = "'panel_event3'"
            elif q.qnum == 20:
                next_stage = "'panel_event4'"
                
            next_progress = q.qnum * 5
            victory_call = 'try { playVictory(); } catch(e) {}' if q.qnum == 20 else 'try { playSuccess(); } catch(e) {}'
            
            # 구역 정보 매핑
            if q.qnum <= 5:
                reset_qnum, reset_prog, zone_name = 1, 0, "1구역"
            elif q.qnum <= 10:
                reset_qnum, reset_prog, zone_name = 6, 25, "2구역"
            elif q.qnum <= 15:
                reset_qnum, reset_prog, zone_name = 11, 50, "3구역"
            else:
                reset_qnum, reset_prog, zone_name = 16, 75, "4구역"

            gas_end_call = ""
            if q.qnum == 20:
                gas_end_call = f'''
                // GAS 기록 종료 호출
                try {{
                    if (window.userRecordRow && typeof google !== 'undefined' && google.script && google.script.run) {{
                        google.script.run.recordEnd(window.userRecordRow, '{unit_code}');
                    }}
                }} catch(e) {{
                    console.warn("구글 시트 종료 기록 실패:", e);
                }}
                
                // 멀티 엔딩 처리
                let outroDiv = document.getElementById("outro-dynamic-text");
                if (outroDiv) {{
                    let firstName = window.playerFirstName || "{chapter.hero}";
                    if (totalWrongCount < 5) {{
                        outroDiv.innerHTML = "미션을 완벽하게 달성했습니다!<br><br>{helper_style}: '" + firstName + "님! 고대의 보물을 찾았습니다. 미션 대성공!'";
                    }} else {{
                        outroDiv.innerHTML = "간신히 관문을 통과했습니다!<br><br>{helper_style}: '" + firstName + "님! 상처투성이 탈출이었지만 간신히 미션을 성공시켰습니다!'";
                    }}
                }}'''

            if q.choices:
                get_ans_js = f'''
            const checkedOpt = document.querySelector('input[name="ans_group{q.qnum}"]:checked');
            const ans = checkedOpt ? checkedOpt.value : "";'''
            else:
                get_ans_js = f'''
            const ans = cleanString(document.getElementById('ans{q.qnum}').value).replace('(','').replace(')','');'''

            # 리셋 타겟 문항 속성
            reset_is_radio = False
            for target_q in chapter.questions:
                if target_q.qnum == reset_qnum:
                    reset_is_radio = len(target_q.choices) > 0
                    break
                    
            if reset_is_radio:
                reset_js = f"document.querySelectorAll('input[name=\"ans_group{reset_qnum}\"]').forEach(el => el.checked = false);"
            else:
                reset_js = f"document.getElementById('ans{reset_qnum}').value = '';"

            js_snippet = f'''
        // Q{q.qnum}
        function checkQ{q.qnum}() {{
            {get_ans_js}
            if ({q.answer}) {{
                wrongCount = 0;
                {victory_call} {gas_end_call}
                nextStage('panel_q{q.qnum}', {next_stage}, {next_progress});
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
                    nextStage('panel_q{q.qnum}', 'panel_q{reset_qnum}', {reset_prog});
                }} else {{
                    showError('panel_q{q.qnum}', 'error{q.qnum}', wrongCount);
                }}
            }}
        }}
'''
            js_checks += js_snippet

        # ─── 3. OUTRO 및 HTML 빌드 병합 ───────────────────────
        outro_img_url = f"https://jk1027.github.io/room-math-story/apps/assets/{assets_folder}/{chapter.outro_image}"
        outro_html = f'''
        <!-- 아웃트로 -->
        <div id="outro" class="glass-panel">
            <h1>탈출 성공!</h1>
            <h2>{chapter.title}</h2>
            <img src="{outro_img_url}" alt="Background" class="panel-image">
            <div class="story-box">
                <div class="story-text" id="outro-dynamic-text">미션 결과를 연산 중입니다...</div>
                <button class="story-log-trigger" onclick="openLog(); event.stopPropagation();">📜 이전 대사</button>
            </div>
            <button class="btn" style="margin-top: 2rem;" onclick="location.reload()">다시 도전하기</button>
        </div>
'''
        
        # 전체 조립 패널 문자열
        panels_html = "".join(question_panels) + "".join(event_panels) + outro_html
        
        # 1. 패널 HTML 치환
        new_content = self.replace_between(content, '<!-- Q1 -->', '<script>', '<!-- Q1 -->\n' + panels_html + '\n    </div>\n    ')
        
        # 2. JS 로직 치환
        start_marker = "// Q1"
        end_marker = "window.onload = () => {"
        end_idx_raw = new_content.find(end_marker)
        if end_idx_raw != -1:
            start_search = end_idx_raw
            while start_search > 0 and new_content[start_search - 1] in [' ', '\t']:
                start_search -= 1
            end_marker_with_indent = new_content[start_search:end_idx_raw + len(end_marker)]
        else:
            end_marker_with_indent = end_marker

        new_content = self.replace_between(new_content, start_marker, end_marker_with_indent, start_marker + '\n' + js_checks + '\n\n        ')

        # 3. CSS 주입 (오류 검출 패널티 CSS 추가)
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
        if ".glitch-text" not in new_content:
            new_content = new_content.replace('</style>', glitch_css)

        # 4. GameOver HTML 및 오버레이 주입
        glitch_html_js = f'''
<!-- V3.0 UI Additions -->
<div id="glitchOverlay" class="glitch-overlay-screen">
    <div class="glitch-overlay-text">🚨 SYSTEM EXPLOITED 🚨</div>
    <div class="glitch-overlay-sub">ACCESS DENIED - CODE ERROR</div>
</div>

<!-- Game Over Panel -->
<div id="gameover" class="glass-panel">
    <h1 style="color: #ef4444; text-shadow: 0 0 15px #ef4444;">미션 실패 (GAME OVER)</h1>
    <h2>산소 고갈!</h2>
    <img src="{outro_img_url}" alt="Game Over" class="panel-image" style="filter: grayscale(1) sepia(1) hue-rotate(-50deg);">
    <div class="story-box">
        <div class="story-text" style="color: #ef4444;">
            시간이 모두 초과되었습니다. 아쉽게도 탈출 조건을 맞추지 못했습니다. 끈기를 내어 처음부터 다시 도전하세요!
        </div>
    </div>
    <button class="btn" style="margin-top: 2rem; background: #ef4444; border-color: #ef4444;" onclick="location.reload()">처음부터 다시 시도하기</button>
</div>
'''
        if "glitchOverlay" not in new_content:
            new_content = new_content.replace('</body>', glitch_html_js + '\n</body>')

        # 5. 타이머 스펙 교체
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
        timer_pattern = r'function startTimer\(\) \{[\s\S]*?updateTimerDisplay\(\);\s*\}\s*,\s*1000\);\s*\}'
        new_content = re.sub(timer_pattern, timer_replacement.strip(), new_content)

        # 6. 복성 및 이름 동적 개인화 처리
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

        # 7. 오답 무전 알림 처리 (showError)
        show_error_replacement = f'''
function showError(panelId, errorId, wrongCount) {{
    try {{ playError(); }} catch(e) {{}} 
    triggerLockdownAlert();
    const panel = document.getElementById(panelId);
    const errMsg = document.getElementById(errorId);
    
    panel.classList.remove('shake');
    void panel.offsetWidth; 
    panel.classList.add('shake');
    
    errMsg.style.display = 'block';
    
    let radioDiv = panel.querySelector('.radio-msg');
    if (!radioDiv) {{
        radioDiv = document.createElement('div');
        radioDiv.className = 'radio-msg';
        errMsg.parentNode.insertBefore(radioDiv, errMsg.nextSibling);
    }}
    
    let firstName = window.playerFirstName || "{chapter.hero}";
    
    if (wrongCount === 1) {{
        radioDiv.innerHTML = "📡 [{chapter.helper}]: '" + firstName + "님, 사소한 계산 실수일 겁니다. 다시 계산해주십시오!'";
    }} else if (wrongCount === 2) {{
        radioDiv.innerHTML = "📡 [{chapter.helper}]: '경고! 다음 오답은 페널티가 발생합니다! 신중하게 골라주세요!'";
    }} else {{
        radioDiv.innerHTML = "";
    }}
    
    setTimeout(() => {{ 
        errMsg.style.display = 'none'; 
        if (radioDiv) radioDiv.innerHTML = "";
    }}, 3500);
}}
'''
        # 기존 showError 함수가 있으면 교체
        show_error_pattern = r'function showError\([\s\S]*?errMsg\.style\.display = \'none\';\s*\}\s*,\s*3500\);\s*\}'
        new_content = re.sub(show_error_pattern, show_error_replacement.strip(), new_content)

        # 8. 최종 산출물 파일 기록
        output_file_path = output_dir / base_html_name
        try:
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            # 동시에 gas/ 폴더 밑의 Index_{unit_code}.html 로도 배포 복사 (DOD 충족)
            gas_target_dir = paths.ROOT_DIR / "gas"
            if gas_target_dir.exists():
                gas_file_name = f"Index_{unit_code}.html"
                with open(gas_target_dir / gas_file_name, 'w', encoding='utf-8') as gf:
                    gf.write(new_content)
                print(f"  [OK] Apps Script game deployment copied: {gas_file_name}")
                
            print(f"  [OK] Game compiled successfully: {output_file_path.name}")
            return True
        except Exception as e:
            print(f"  [Error] Failed to write game HTML: {e}")
            return False
