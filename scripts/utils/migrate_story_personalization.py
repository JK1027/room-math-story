import re
import os
import glob

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
builders_dir = os.path.join(project_root, "scripts", "builders")

# 단어 대체 규칙 테이블 (어드벤처 톤앤매너 순화)
soften_rules = {
    "으스러지기 싫다면": "포기하기 싫다면",
    "수장당했다": "탈출에 실패했다",
    "수장당할 것": "실패할 것",
    "뼈를 으개어주마": "원점으로 돌려보내주마",
    "뼈를 으깨어주마": "원점으로 돌려보내주마",
    "뼈를 으스려트리겠다": "시스템을 리셋하겠다",
    "자폭 폭파하겠다": "시스템을 포맷하겠다",
    "잿더미로 만들어주지": "초기화 시켜주지",
    "데이터를 자폭": "데이터를 초기화",
    "소멸한다아아": "정지한다아아",
    "소멸한다": "정지한다",
    "소멸을 막기": "포맷을 막기",
    "목숨을 건졌습니다": "보물을 획득했습니다",
    "죽음의": "위험한",
    "으깨지지 않으려면": "튕겨나가지 않으려면",
    "비명을 지르며": "경고음을 내며",
    "공포": "긴장"
}

# 감지할 호칭 목록
roles = ["캡틴", "대장", "요원", "학도", "탐정", "모험가", "조수", "마법사", "동료", "연구원", "조사원", "수습생", "탐사대원"]
role_pattern = r'(?<![a-zA-Z0-9_\-"\'/])(' + '|'.join(roles) + r')(?![a-zA-Z0-9_\-"\'/])'

js_personalization_code = """
            // 이름 동적 개인화 처리 (복성 예외 처리 반영 및 전역 변수 바인딩)
            try {
                let rawName = "";
                if (typeof sname !== 'undefined' && sname) {
                    rawName = (typeof sname.value !== 'undefined') ? sname.value.trim() : (typeof sname === 'string' ? sname.trim() : "");
                } else if (typeof studentName !== 'undefined') {
                    rawName = (typeof studentName.value !== 'undefined') ? studentName.value.trim() : (typeof studentName === 'string' ? studentName.trim() : "");
                }
                if (!rawName) {
                    const nameInput = document.getElementById('studentName');
                    if (nameInput) rawName = nameInput.value.trim();
                }
                if (rawName) {
                    const doubleLastNames = ["제갈", "황보", "사공", "남궁", "서문", "독고", "선우"];
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
                    // 아웃트로 동적 텍스트 내 개인화 처리
                    let outroTextEl = document.getElementById("outro-dynamic-text");
                    if (outroTextEl) {
                        outroTextEl.querySelectorAll(".dynamic-captain-name").forEach(el => {
                            let originalRole = el.getAttribute("data-original-role") || el.innerText;
                            if (!el.hasAttribute("data-original-role")) {
                                el.setAttribute("data-original-role", originalRole);
                            }
                            el.innerHTML = firstName + " " + originalRole;
                        });
                    }
                }
            } catch(e) { console.error("이름 개인화 에러:", e); }
"""

def extract_unit_id(filename):
    m = re.search(r'update_app_(m\d+)_(\d+)\.py', filename)
    if m:
        return f"{m.group(1)}_{m.group(2)}"
    m = re.search(r'update_app_(\d+)\.py', filename)
    if m:
        return f"m1_{m.group(1)}"
    return "m1_01"

def migrate_file(filepath):
    filename = os.path.basename(filepath)
    if filename == "update_app_04.py":
        return False
        
    unit_id = extract_unit_id(filename)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
        
    original_code = code
    
    # 1. 톤앤매너 순화 규칙 적용
    for k, v in soften_rules.items():
        code = code.replace(k, v)
        
    # 2. 호칭 감지 및 <span class="dynamic-captain-name">호칭</span> 태그 적용
    qs_match = re.search(r'(?s)qs\s*=\s*\[.*?\]', code)
    if qs_match:
        qs_block = qs_match.group(0)
        new_qs_block = re.sub(role_pattern, r'<span class="dynamic-captain-name">\1</span>', qs_block)
        code = code.replace(qs_block, new_qs_block)
        
    base_html_match = re.search(r'(?s)base_html\s*=\s*""".*?"""', code)
    if base_html_match:
        base_html_block = base_html_match.group(0)
        new_base_html_block = re.sub(role_pattern, r'<span class="dynamic-captain-name">\1</span>', base_html_block)
        code = code.replace(base_html_block, new_base_html_block)

    # 3. 인트로 폼 주입 (학생 정보 입력 영역이 없는 경우)
    if "studentName" not in code and "studentId" not in code:
        btn_pattern = r'(<div class="btn-group">\s*<button class="btn" onclick="nextStage\(\'intro\', \'panel_q1\', \d+\)">.*?<\/button>\s*<\/div>)'
        student_form_html = f"""
            <div class="student-info-form" style="margin-top: 1.5rem; text-align: left; background: rgba(0,0,0,0.3); padding: 1.2rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                <div style="margin-bottom: 1rem;">
                    <label for="studentId" style="display: block; margin-bottom: 0.5rem; color: #60A5FA; font-weight: bold; font-size: 1rem;">학번</label>
                    <input type="text" id="studentId" placeholder="예: 1130" style="width: 100%; padding: 0.8rem; border-radius: 8px; border: 1px solid rgba(96, 165, 250, 0.4); background: rgba(15,23,42,0.6); color: white; font-size: 1.1rem; font-weight: bold; box-sizing: border-box;">
                </div>
                <div>
                    <label for="studentName" style="display: block; margin-bottom: 0.5rem; color: #60A5FA; font-weight: bold; font-size: 1rem;">이름</label>
                    <input type="text" id="studentName" placeholder="예: 홍길동" style="width: 100%; padding: 0.8rem; border-radius: 8px; border: 1px solid rgba(96, 165, 250, 0.4); background: rgba(15,23,42,0.6); color: white; font-size: 1.1rem; font-weight: bold; box-sizing: border-box;">
                </div>
            </div>
            <div class="btn-group" style="margin-top: 2rem; width:100%;">
                <button class="btn" onclick="tryStartGame('{unit_id}')">미션 시작</button>
            </div>
"""
        code = re.sub(btn_pattern, student_form_html, code)

    # 4. JS 이름 주입 로직 주입
    m1_m2_pattern = r'(if\s*\(!sid\.value\.trim\(\)\s*\|\|\s*!sname\.value\.trim\(\)\)\s*\{[\s\S]*?return;\s*\})'
    m1_m2_alt_pattern = r'(if\s*\(!sid\s*\|\|\s*!sname\)\s*\{[\s\S]*?return;\s*\})'
    m3_pattern = r'(studentName\s*=\s*prompt\("이름을 입력하세요:"\);[\s\S]*?if\s*\(!studentId\s*\|\|\s*!studentName\)\s*\{[\s\S]*?return;\s*\})'
    onload_pattern = r'(const sname\s*=\s*document\.getElementById\(\'studentName\'\);[\s\S]*?return;\s*\})'
    
    injected = False
    
    if re.search(m1_m2_pattern, code):
        code = re.sub(m1_m2_pattern, r'\1\n' + js_personalization_code, code)
        injected = True
    elif re.search(m1_m2_alt_pattern, code):
        code = re.sub(m1_m2_alt_pattern, r'\1\n' + js_personalization_code, code)
        injected = True
    elif re.search(m3_pattern, code):
        code = re.sub(m3_pattern, r'\1\n' + js_personalization_code, code)
        injected = True
    elif re.search(onload_pattern, code):
        code = re.sub(onload_pattern, r'\1\n' + js_personalization_code, code)
        injected = True
        
    if "function tryStartGame" not in code:
        try_start_game_js = f"""
        function tryStartGame(unitId) {{
            const sid = document.getElementById('studentId');
            const sname = document.getElementById('studentName');
            if(sid && sname) {{
                if(!sid.value.trim() || !sname.value.trim()) {{
                    alert('학번과 이름을 모두 입력해주세요!');
                    return;
                }}
                try {{
                    if(typeof google !== 'undefined' && google.script && google.script.run) {{
                        google.script.run
                            .withSuccessHandler(function(row) {{ window.userRecordRow = row; }})
                            .recordStart(sid.value.trim(), sname.value.trim(), unitId);
                    }}
                }} catch(e) {{ console.warn('GAS 연동 안됨:', e); }}
            }}
            
            // 이름 동적 개인화 처리 (복성 예외 처리 반영 및 전역 변수 바인딩)
            try {{
                const doubleLastNames = ["제갈", "황보", "사공", "남궁", "서문", "독고", "선우"];
                let rawName = sname.value.trim();
                let firstName = rawName;
                if (rawName.length > 2) {{
                    let prefix2 = rawName.substring(0, 2);
                    if (doubleLastNames.includes(prefix2)) {{
                        firstName = rawName.substring(2);
                    }} else {{
                        firstName = rawName.substring(1);
                    }}
                }}
                window.playerFirstName = firstName;
                document.querySelectorAll(".dynamic-captain-name").forEach(el => {{
                    let originalRole = el.getAttribute("data-original-role") || el.innerText;
                    if (!el.hasAttribute("data-original-role")) {{
                        el.setAttribute("data-original-role", originalRole);
                    }}
                    el.innerHTML = firstName + " " + originalRole;
                }});
            }} catch(e) {{ console.error("이름 개인화 에러:", e); }}
            
            nextStage('intro', 'panel_q1', 0);
        }}
"""
        code = code.replace("function nextStage", try_start_game_js + "\n        function nextStage")
        injected = True
            
    if code != original_code:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"Migrated: {filename} (Personalization JS Injected: {injected})")
        return True
    return False

if __name__ == "__main__":
    builder_files = glob.glob(os.path.join(builders_dir, "update_app_*.py"))
    migrated_count = 0
    for filepath in builder_files:
        if migrate_file(filepath):
            migrated_count += 1
            
    print(f"\nMigration completed. Total migrated files: {migrated_count}")
