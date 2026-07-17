import os
import re
import subprocess
import sys
import argparse
from pathlib import Path

# ----------------- 단원별 설정 사전 -----------------
UNIT_CONFIGS = {
    "m1_04": {
        "script_name": "m1_04_atlantis_script.md",
        "assets_folder": "m1_04_coordinates",
        "title": "중1 4단원: 좌표와 그래프 - 심해의 구도자",
        "main_title": "[오프닝 & 인트로] 아틀란티스 신전의 부름",
        "outro_title": "[엔딩 & 아웃트로] 심해 탈출 성공",
        "hud_title": "COORDINATES & GRAPHS"
    },
    "m1_05": {
        "script_name": "m1_05_geometry_script.md",
        "assets_folder": "m1_05_basic_geometry",
        "title": "중1 5단원: 기본 도형 - 다빈치의 비밀 작업실",
        "main_title": "[오프닝 & 인트로] 다빈치의 비밀 작업실",
        "outro_title": "[엔딩 & 아웃트로] 기하학의 비밀 복원",
        "hud_title": "BASIC GEOMETRY"
    }
}

# ----------------- 경로 설정 -----------------
project_root = r"c:\Coding\Projects\School\room-math-story"
html_temp_path = os.path.join(project_root, "scratch", "temp_storybook.html")

# ----------------- 데이터 파싱 -----------------

def load_intro_outro(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\r\n', '\n')
        
    intro_match = re.search(r'## 🎬 \[오프닝 & 인트로\]\n([\s\S]*?)(?:\n---|\n## |$)', content)
    intro_text = intro_match.group(1).strip() if intro_match else ""
    
    outro_match = re.search(r'## 🎬 \[엔딩 & 아웃트로\]\n([\s\S]*?)(?:\n---|\n## |$)', content)
    outro_text = outro_match.group(1).strip() if outro_match else ""
    
    return intro_text, outro_text

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

    # 2. 문항 정의 파싱
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

    # 3. 이벤트 정의 파싱
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
            elif line_str.startswith('- BUTTON_TEXT:'):  # 대소문자 방지
                ev_data["btn_text"] = line_str.replace('- BUTTON_TEXT:', '').strip()
            elif line_str.startswith('- 다음 스테이지:'):
                ev_data["next_stage"] = line_str.replace('- 다음 스테이지:', '').strip()
            elif line_str.startswith('- 달성도:'):
                ev_data["progress"] = int(line_str.replace('- 달성도:', '').strip())
            elif line_str.startswith('- 지문:'):
                story_started = True
                
        ev_data["story"] = '\n'.join(story_lines).strip()
        events[evnum] = ev_data

    return img_map, qs, events

# ----------------- HTML 스타일 가공 -----------------

def apply_character_styles(text):
    # 캐릭터 스팬 정의
    nereus = "<span style='color: #60a5fa; text-shadow: 0 0 3px #3b82f6; font-weight: bold;'>[네레우스]</span>"
    clio = "<span style='color: #c084fc; text-shadow: 0 0 3px #a855f7; font-weight: bold;'>[클리오]</span>"
    poseidon = "<span style='color: #f43f5e; text-shadow: 0 0 3px #f43f5e; font-weight: bold;'>[포세이돈-V]</span>"
    trident = "<span style='color: #fb923c; text-shadow: 0 0 3px #f97316; font-weight: bold;'>[트라이던트]</span>"
    captain = "<span style='color: #34d399; text-shadow: 0 0 3px #059669; font-weight: bold;'>[캡틴]</span>"
    
    # 5단원 캐릭터
    codex = "<span style='color: #ef4444; text-shadow: 0 0 3px #ef4444; font-weight: bold;'>[코덱스-L]</span>"
    davinci = "<span style='color: #60a5fa; text-shadow: 0 0 3px #3b82f6; font-weight: bold;'>[다빈치-메모리]</span>"

    text = text.replace("{nereus}", nereus).replace("[네레우스]", nereus)
    text = text.replace("{clio}", clio).replace("[클리오]", clio)
    text = text.replace("{poseidon}", poseidon).replace("[포세이돈-V]", poseidon)
    text = text.replace("{trident}", trident).replace("[트라이던트]", trident)
    text = text.replace("{dyn_captain}", captain).replace("캡틴", captain).replace("[캡틴]", captain)
    text = text.replace("{codex}", codex).replace("[코덱스-L]", codex)
    text = text.replace("{davinci}", davinci).replace("[다빈치-메모리]", davinci)
    
    # 대화 패턴 치환
    text = re.sub(r'-\s*\*\*포세이돈-V:\*\*|-\s*\*\*포세이돈-V\*\*:', f'{poseidon}', text)
    text = re.sub(r'-\s*\*\*네레우스:\*\*|-\s*\*\*네레우스\*\*:', f'{nereus}', text)
    text = re.sub(r'-\s*\*\*클리오:\*\*|-\s*\*\*클리오\*\*:', f'{clio}', text)
    text = re.sub(r'-\s*\*\*트라이던트:\*\*|-\s*\*\*트라이던트\*\*:', f'{trident}', text)
    text = re.sub(r'-\s*\*\*조사관\s*\(플레이어\):\*\*|-\s*\*\*조사관\*\*:', f'{captain}', text)
    text = re.sub(r'-\s*\*\*코덱스-L:\*\*|-\s*\*\*코덱스-L\*\*:', f'{codex}', text)
    text = re.sub(r'-\s*\*\*다빈치-메모리:\*\*|-\s*\*\*다빈치-메모리\*\*:', f'{davinci}', text)
    
    # 일반 텍스트 내 캐릭터명 치환
    text = text.replace("네레우스:", nereus).replace("클리오:", clio).replace("포세이돈-V:", poseidon).replace("트라이던트:", trident)
    text = text.replace("코덱스-L:", codex).replace("다빈치-메모리:", davinci)
    
    return text

def format_story_content(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    formatted = []
    for line in lines:
        if line.startswith('*') and line.endswith('*'):
            line = f"<em style='color: #94a3b8; font-style: italic;'>{line[1:-1]}</em>"
        elif line.startswith('<i>') and line.endswith('</i>'):
            line = f"<em style='color: #94a3b8; font-style: italic;'>{line[3:-4]}</em>"
        
        # 기호 장식 제거 및 캐릭터 스타일
        if any(line.startswith(emoji) for emoji in ['🌊', '🧭', '⚙️', '💎', '💥', '🚨', '🔴', '📐', '✂️', '🖼️', '🔮', '⚠️']):
            line = f"<strong style='color: #38bdf8; display: block; margin-top: 8px; margin-bottom: 8px; font-size: 1.05rem;'>{line}</strong>"
        else:
            line = apply_character_styles(line)
            
        formatted.append(f"<p style='margin: 6px 0;'>{line}</p>")
    return '\n'.join(formatted)

def format_script_text(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    formatted_lines = []
    for line in lines:
        # 일러스트 지시
        if "일러스트 지시" in line:
            clean_line = re.sub(r'-\s*\*\*\[일러스트\s*지시[^\]]*\]:\*\*', '', line).strip()
            clean_line = re.sub(r'-\s*\*\*일러스트\s*지시[^\]]*\*\*:', '', clean_line).strip()
            formatted_lines.append(f"<div style='margin-top:14px; font-size:0.8rem; color:#f59e0b; background:rgba(245,158,11,0.08); padding:8px 12px; border-left:3px solid #f59e0b; border-radius:4px;'><strong>🎨 일러스트 가이드:</strong> {clean_line}</div>")
            continue
            
        # 선체 상태 (혹은 상태 표시)
        if "선체 상태:" in line or "선체 상태" in line:
            clean_line = line.replace("- **선체 상태:**", "").replace("- **선체 상태**:", "").replace("`", "").strip()
            formatted_lines.append(f"<div style='font-family:\"Share Tech Mono\", monospace; font-size:0.85rem; color:#ef4444; background:rgba(239,68,68,0.08); padding:6px 12px; border: 1px solid rgba(239,68,68,0.2); border-radius:4px; margin-bottom:12px;'>📟 <strong>시스템 상태:</strong> {clean_line}</div>")
            continue
            
        # 스토리 전개
        if "스토리 전개:" in line:
            clean_line = line.replace("- **스토리 전개:**", "").strip()
            formatted_lines.append(f"<p style='color:#94a3b8; font-style:italic; border-left:2px solid #475569; padding-left:10px;'>{clean_line}</p>")
            continue

        # 대화 및 일반 라인
        if line.startswith('- '):
            clean_line = line[2:].strip()
            clean_line = apply_character_styles(clean_line)
            formatted_lines.append(f"<p style='margin: 6px 0;'>{clean_line}</p>")
        else:
            line = apply_character_styles(line)
            formatted_lines.append(f"<p style='margin: 6px 0;'>{line}</p>")
            
    return '\n'.join(formatted_lines)

# ----------------- 브라우저 경로 탐색 -----------------

def find_browser():
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
            
    for name in ["chrome.exe", "msedge.exe"]:
        try:
            res = subprocess.check_output(["where", name], stderr=subprocess.DEVNULL)
            paths = res.decode('utf-8').strip().split('\r\n')
            if paths and os.path.exists(paths[0]):
                return paths[0]
        except Exception:
            continue
            
    return None

# ----------------- 메인 로직 -----------------

def main():
    parser = argparse.ArgumentParser(description="Generate PDF storyboard book.")
    parser.add_argument('--unit', type=str, default='m1_04', help='Unit ID (e.g. m1_04, m1_05)')
    args = parser.parse_args()
    
    unit = args.unit
    if unit not in UNIT_CONFIGS:
        print(f"Error: Unit '{unit}' is not configured in build_pdf_storybook.py")
        sys.exit(1)
        
    config = UNIT_CONFIGS[unit]
    
    storyboard_path = os.path.join(project_root, "data", "storyboards", f"{unit}_storyboard.md")
    script_path = os.path.join(project_root, "stories", "중1", config["script_name"])
    assets_dir = os.path.join(project_root, "apps", "assets", config["assets_folder"])
    pdf_output_path = os.path.join(project_root, "data", "storyboards", f"{unit}_storyboard.pdf")
    
    print(f"Parsing files for unit {unit}...")
    if not os.path.exists(storyboard_path) or not os.path.exists(script_path):
        print(f"Error: Required storyboard or script files for {unit} do not exist.")
        print(f"Storyboard: {storyboard_path}")
        print(f"Script: {script_path}")
        sys.exit(1)
        
    intro_raw, outro_raw = load_intro_outro(script_path)
    img_map, qs, events = load_storyboard(storyboard_path)
    
    pages_html = []
    
    # Page 1: Intro
    intro_img_path = os.path.join(assets_dir, "intro.png")
    if not os.path.exists(intro_img_path):
        intro_img_path = os.path.join(assets_dir, "img1_radar.png")
    intro_uri = Path(intro_img_path).as_uri()
    intro_html_text = format_script_text(intro_raw)
    
    pages_html.append(f'''
    <div class="page">
      <div class="image-area">
        <img src="{intro_uri}" alt="Intro Image">
      </div>
      <div class="text-area">
        <div class="hud-header">
          <span class="hud-title">SYSTEM INITIATING...</span>
          <span class="hud-status">STATUS: ONLINE</span>
        </div>
        <h2>{config["main_title"]}</h2>
        <div class="story-content">
          {intro_html_text}
        </div>
      </div>
    </div>
    ''')
    
    # 인덱스 계산용 헬퍼 함수
    def add_question_page(q):
        qnum = q["qnum"]
        # 이미지 매핑
        img_name = img_map.get(qnum, f"q{qnum}.png")
        img_path = os.path.join(assets_dir, img_name)
        if not os.path.exists(img_path):
            img_path = os.path.join(assets_dir, f"q{qnum}.png")
        if not os.path.exists(img_path):
            img_path = os.path.join(assets_dir, "img1_radar.png")
            
        img_uri = Path(img_path).as_uri()
        story_html = format_story_content(q["story"])
        
        options_html = ""
        if q.get("options"):
            options_html = "<div class='quiz-options'>"
            for opt in q["options"]:
                options_html += f"<span class='quiz-opt'>{opt}</span>"
            options_html += "</div>"
            
        pages_html.append(f'''
        <div class="page">
          <div class="image-area">
            <img src="{img_uri}" alt="Q{qnum} Image">
          </div>
          <div class="text-area">
            <div class="hud-header">
              <span class="hud-title">{config["hud_title"]}</span>
              <span class="hud-status">STAGE {qnum}/20</span>
            </div>
            <h2>Q{qnum}. {q.get("title", "기하학의 수수께끼")}</h2>
            <div class="story-content">
              {story_html}
            </div>
            <div class="quiz-box">
              <div class="quiz-question">{q.get("qtext", "")}</div>
              {options_html}
              <div class="quiz-meta">
                <strong>💡 힌트:</strong> {q.get("hint", "")}<br>
                <strong>🔑 정답 조건:</strong> <code class="code-ans">{q.get("ans_check", "")}</code>
              </div>
            </div>
          </div>
        </div>
        ''')
        
    def add_event_page(evnum):
        ev = events[evnum]
        img_name = img_map.get(f"event{evnum}", f"event{evnum}.png")
        img_path = os.path.join(assets_dir, img_name)
        if not os.path.exists(img_path):
            img_path = os.path.join(assets_dir, f"event{evnum}.png")
            
        img_uri = Path(img_path).as_uri()
        story_html = format_story_content(ev["story"])
        
        pages_html.append(f'''
        <div class="page">
          <div class="image-area">
            <img src="{img_uri}" alt="Event {evnum} Image">
          </div>
          <div class="text-area">
            <div class="hud-header">
              <span class="hud-title">CRITICAL EVENT DETECTED</span>
              <span class="hud-status">PROGRESS {ev.get("progress", 0)}%</span>
            </div>
            <h2>[이벤트 {evnum}] {ev.get("title", "돌발 상황")}</h2>
            <div class="story-content">
              {story_html}
            </div>
            <div class="event-meta">
              <strong>👉 기동 옵션:</strong> {ev.get("btn_text", "")} (다음: {ev.get("next_stage", "")})
            </div>
          </div>
        </div>
        ''')

    # Q1 ~ Q5
    for i in range(0, 5):
        add_question_page(qs[i])
        
    # EVENT1
    add_event_page(1)
    
    # Q6 ~ Q10
    for i in range(5, 10):
        add_question_page(qs[i])
        
    # EVENT2
    add_event_page(2)
    
    # Q11 ~ Q15
    for i in range(10, 15):
        add_question_page(qs[i])
        
    # EVENT3
    add_event_page(3)
    
    # Q16 ~ Q20
    for i in range(15, 20):
        add_question_page(qs[i])
        
    # EVENT4
    add_event_page(4)
    
    # Page 26: Outro
    outro_img_path = os.path.join(assets_dir, "outro.png")
    if not os.path.exists(outro_img_path):
        outro_img_path = os.path.join(assets_dir, "img10_escape.png")
    outro_uri = Path(outro_img_path).as_uri()
    outro_html_text = format_script_text(outro_raw)
    
    pages_html.append(f'''
    <div class="page">
      <div class="image-area">
        <img src="{outro_uri}" alt="Outro Image">
      </div>
      <div class="text-area">
        <div class="hud-header">
          <span class="hud-title">MISSION ACCOMPLISHED</span>
          <span class="hud-status">STATUS: COMPLETED</span>
        </div>
        <h2>{config["outro_title"]}</h2>
        <div class="story-content">
          {outro_html_text}
        </div>
      </div>
    </div>
    ''')
    
    # HTML 조립
    html_content = f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>{config["title"]}</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&family=Share+Tech+Mono&display=swap');
    
    @page {{
      size: A4 landscape;
      margin: 0;
    }}
    
    * {{
      box-sizing: border-box;
    }}
    
    body {{
      margin: 0;
      padding: 0;
      font-family: 'Noto Sans KR', sans-serif;
      background-color: #030712;
      color: #e2e8f0;
      overflow: hidden;
    }}
    
    .page {{
      width: 297mm;
      height: 210mm;
      display: flex;
      page-break-after: always;
      position: relative;
      background-color: #030712;
    }}
    
    ::-webkit-scrollbar {{
      display: none;
    }}
    
    .image-area {{
      width: 55%;
      height: 100%;
      overflow: hidden;
      position: relative;
      border-right: 4px solid #1e293b;
    }}
    
    .image-area img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
    }}
    
    .image-area::after {{
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      border: 10px solid rgba(15, 23, 42, 0.3);
      pointer-events: none;
      box-shadow: inset 0 0 80px rgba(0,0,0,0.6);
    }}
    
    .text-area {{
      width: 45%;
      height: 100%;
      padding: 24px 32px;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      background: linear-gradient(135deg, #090d1a 0%, #030712 100%);
      position: relative;
    }}
    
    .hud-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #1e293b;
      padding-bottom: 8px;
      margin-bottom: 16px;
      font-family: 'Share Tech Mono', monospace;
      font-size: 0.85rem;
      color: #94a3b8;
      letter-spacing: 1px;
    }}
    
    .hud-title {{
      color: #60a5fa;
      text-shadow: 0 0 8px rgba(96, 165, 250, 0.4);
    }}
    
    .hud-status {{
      background-color: rgba(30, 41, 59, 0.5);
      padding: 2px 8px;
      border-radius: 4px;
      border: 1px solid #334155;
    }}
    
    h2 {{
      margin-top: 0;
      margin-bottom: 16px;
      font-size: 1.4rem;
      color: #f8fafc;
      font-weight: 700;
      line-height: 1.3;
      text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }}
    
    .story-content {{
      flex: 1;
      font-size: 0.95rem;
      line-height: 1.7;
      color: #cbd5e1;
      overflow-y: auto;
      padding-right: 8px;
      margin-bottom: 16px;
      background-color: rgba(15, 23, 42, 0.2);
      padding: 12px;
      border-radius: 6px;
      border: 1px solid rgba(255, 255, 255, 0.03);
    }}
    
    .story-content p {{
      margin: 0 0 10px 0;
    }}
    
    .story-content p:last-child {{
      margin-bottom: 0;
    }}
    
    .quiz-box {{
      background: rgba(15, 23, 42, 0.6);
      border: 1.5px solid #1e3a8a;
      box-shadow: 0 0 15px rgba(30, 58, 138, 0.2);
      border-radius: 8px;
      padding: 14px;
      margin-top: auto;
    }}
    
    .quiz-question {{
      font-size: 0.95rem;
      font-weight: 700;
      color: #38bdf8;
      margin-bottom: 10px;
      line-height: 1.5;
    }}
    
    .quiz-options {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 10px;
    }}
    
    .quiz-opt {{
      background-color: #1e293b;
      border: 1px solid #334155;
      color: #e2e8f0;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 0.8rem;
    }}
    
    .quiz-meta {{
      font-size: 0.8rem;
      color: #94a3b8;
      border-top: 1px dashed #334155;
      padding-top: 8px;
      line-height: 1.6;
    }}
    
    .code-ans {{
      font-family: 'Share Tech Mono', monospace;
      color: #34d399;
      background-color: rgba(52, 211, 153, 0.1);
      padding: 2px 6px;
      border-radius: 4px;
    }}
    
    .event-meta {{
      background: rgba(15, 23, 42, 0.6);
      border: 1.5px solid #a855f7;
      box-shadow: 0 0 15px rgba(168, 85, 247, 0.15);
      border-radius: 8px;
      padding: 14px;
      margin-top: auto;
      font-size: 0.9rem;
      color: #e9d5ff;
    }}
    
    .text-area::before {{
      content: '';
      position: absolute;
      top: 12px; right: 12px;
      width: 15px; height: 15px;
      border-top: 2px solid #60a5fa;
      border-right: 2px solid #60a5fa;
      opacity: 0.3;
    }}
    
    .text-area::after {{
      content: '';
      position: absolute;
      bottom: 12px; left: 12px;
      width: 15px; height: 15px;
      border-bottom: 2px solid #60a5fa;
      border-left: 2px solid #60a5fa;
      opacity: 0.3;
    }}
  </style>
</head>
<body>
  {"".join(pages_html)}
</body>
</html>
'''
    
    # 임시 HTML 저장
    print(f"Writing temporary HTML to {html_temp_path}...")
    os.makedirs(os.path.dirname(html_temp_path), exist_ok=True)
    with open(html_temp_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    # 브라우저 실행
    browser_path = find_browser()
    if not browser_path:
        print("Error: Chrome or Microsoft Edge was not found on this system.")
        sys.exit(1)
        
    print(f"Using browser at: {browser_path}")
    print(f"Printing to PDF: {pdf_output_path}...")
    
    # PDF 출력 명령 실행
    cmd = [
        browser_path,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={pdf_output_path}",
        html_temp_path
    ]
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # 임시 HTML 파일 삭제
    try:
        os.remove(html_temp_path)
        print("Cleaned up temporary HTML file.")
    except Exception as e:
        print(f"Warning: Failed to delete temporary HTML: {e}")
        
    if result.returncode == 0 and os.path.exists(pdf_output_path):
        print(f"Success! PDF storyboard has been successfully generated at:\n{pdf_output_path}")
    else:
        print(f"Error printing to PDF. Return code: {result.returncode}")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    main()
