import os
import re
import sys
import yaml
from pathlib import Path

# --- Central Configs Loading ---
_cur = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(os.path.dirname(_cur))
if _root not in sys.path:
    sys.path.append(_root)
from scripts.config import paths
from scripts.config.constants import SUPPORTED_GRADES

def read_file_safe(filepath):
    """
    파일의 인코딩(utf-8 vs cp949/euc-kr)을 판별하여 깨짐 없이 온전하게 로드합니다.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if "질문" in content or "지문" in content or "이미지" in content:
                return content.replace('\r\n', '\n')
    except UnicodeDecodeError:
        pass
        
    try:
        with open(filepath, 'r', encoding='cp949') as f:
            content = f.read()
            return content.replace('\r\n', '\n')
    except Exception:
        pass
        
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read().replace('\r\n', '\n')

def parse_markdown_storyboard(filepath):
    """
    기존 마크다운 스토리보드를 파싱하여 이미지 매핑, 질문 메타데이터, 이벤트 데이터를 로드합니다.
    """
    content = read_file_safe(filepath)

    # 1. 이미지 매핑 파싱 (숫자 키는 q1, q2... 로 강제 변환)
    img_map = {}
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
                    # 숫자 키 q화 (1 -> q1)
                    if key.isdigit():
                        img_map[f"q{key}"] = val
                    else:
                        img_map[key] = val

    # 2. 문항 정의 파싱
    questions = {}
    q_parts = content.split('## Q')
    for part in q_parts[1:]:
        part_lines = part.strip().split('\n')
        qnum_str = part_lines[0].strip()
        if not qnum_str.isdigit():
            continue
        qnum = int(qnum_str)
        
        q_data = {}
        story_started = False
        
        for line in part_lines[1:]:
            if story_started:
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

        # 힌트가 누락된 경우 Fallback 힌트 자동 보강 (Schema 에러 방지)
        if not q_data.get("hint"):
            q_data["hint"] = "💡 힌트가 제공되지 않는 구역입니다. 연산을 신중히 전개해 보세요."
        if not q_data.get("ans_check"):
            q_data["ans_check"] = "ans === '0'" # Fallback answer

        questions[f"q{qnum}"] = q_data

    # 3. 이벤트 정의 파싱
    events = {}
    event_parts = content.split('## EVENT')
    for part in event_parts[1:]:
        part_lines = part.strip().split('\n')
        evnum_str = part_lines[0].strip()
        if not evnum_str.isdigit():
            continue
        evnum = int(evnum_str)
        
        ev_data = {}
        for line in part_lines[1:]:
            line_str = line.strip()
            if line_str.startswith('- 제목:'):
                ev_data["title"] = line_str.replace('- 제목:', '').strip()
            elif line_str.startswith('- 버튼 텍스트:'):
                ev_data["btn_text"] = line_str.replace('- 버튼 텍스트:', '').strip()
            elif line_str.startswith('- 다음 스테이지:'):
                ev_data["next_stage"] = line_str.replace('- 다음 스테이지:', '').strip()
            elif line_str.startswith('- 달성도:'):
                ev_data["progress"] = int(line_str.replace('- 달성도:', '').strip())

        events[f"event{evnum}"] = ev_data

    return img_map, questions, events

def main():
    storyboard_root = paths.STORYBOARDS_DIR
    quiz_data_root = paths.ROOT_DIR / "quiz_data"
    
    # 23개 단원 루프
    for grade in SUPPORTED_GRADES:
        sb_dir = storyboard_root / grade
        if not sb_dir.exists():
            continue
            
        target_dir = quiz_data_root / grade
        target_dir.mkdir(parents=True, exist_ok=True)
        
        for filename in os.listdir(sb_dir):
            if not filename.endswith("_storyboard.md"):
                continue
                
            unit = filename.replace("_storyboard.md", "")
            if unit == "m1_01":
                continue
                
            filepath = sb_dir / filename
            print(f"Migrating storyboard to YAML: {filename}...")
            
            try:
                img_map, questions, events = parse_markdown_storyboard(filepath)
                
                template_type = "escape_room"
                if unit == "m1_04":
                    template_type = "custom_coordinates"
                elif unit == "m1_05":
                    template_type = "custom_geometry"
                
                yaml_data = {
                    "template": template_type,
                    "image_mapping": img_map,
                    "questions": questions,
                    "events": events
                }
                
                yaml_path = target_dir / f"{unit}.yaml"
                with open(yaml_path, 'w', encoding='utf-8') as yf:
                    yaml.dump(yaml_data, yf, allow_unicode=True, default_flow_style=False, sort_keys=False)
                    
            except Exception as e:
                print(f"Error migrating {filename}: {e}", file=sys.stderr)

    print("[+] Migration tool process completed successfully.")

if __name__ == "__main__":
    main()
