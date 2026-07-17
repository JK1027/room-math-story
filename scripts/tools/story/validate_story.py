import os
import sys
import re
from pathlib import Path

# 바이블 위반 금지어 (AI 관련 메타 단어 및 비속어 등)
BANNED_KEYWORDS = ["chatgpt", "gpt", "인공지능", "openai", "bard", "gemini"]

def check_bible_violations(text, file_name):
    """Checks for banned keywords in script text."""
    violations = []
    text_lower = text.lower()
    for kw in BANNED_KEYWORDS:
        if kw in text_lower:
            violations.append(f"Banned keyword '{kw}' found in {file_name}")
    return violations

def validate_storyboard(file_path, project_root):
    """
    Statically analyzes a single storyboard markdown file.
    Checks for:
    - Sequential Q numbers (Q1 to Q20)
    - Target image files existence in apps/assets/
    - Valid next stage transitions in events
    - Metadata and hint formats
    - Bible keyword violations
    """
    errors = []
    file_name = os.path.basename(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\r\n', '\n')
        
    # Bible keyword check on the entire content
    violations = check_bible_violations(content, file_name)
    errors.extend(violations)
    
    # 1. Parse Image Mappings
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
                    img_map[key] = val
                    
    # 2. Check Q1 ~ Q20
    q_parts = content.split('## Q')
    q_nums = []
    
    # Find active asset directory
    unit_id = file_name.replace("_storyboard.md", "")
    assets_dir = None
    assets_root = project_root / "apps" / "assets"
    
    if assets_root.exists():
        for dname in os.listdir(assets_root):
            if dname.startswith(unit_id) and os.path.isdir(assets_root / dname):
                assets_dir = assets_root / dname
                break
                
    for part in q_parts[1:]:
        lines = part.strip().split('\n')
        qnum_str = lines[0].strip()
        if not qnum_str.isdigit():
            errors.append(f"Invalid section header: '## Q{qnum_str}' is not numeric.")
            continue
            
        qnum = int(qnum_str)
        q_nums.append(qnum)
        
        # Check specific Q lines
        has_title = False
        has_qtext = False
        has_ans = False
        has_story = False
        story_started = False
        
        for line in lines[1:]:
            line_str = line.strip()
            if line_str.startswith('- 제목:'):
                has_title = True
            elif line_str.startswith('- 질문:'):
                has_qtext = True
            elif line_str.startswith('- 정답 체크:'):
                has_ans = True
            elif line_str.startswith('- 지문:'):
                has_story = True
                story_started = True
                
        if not has_title:
            errors.append(f"Q{qnum} in {file_name} is missing Title (- 제목:).")
        if not has_qtext:
            errors.append(f"Q{qnum} in {file_name} is missing Question (- 질문:).")
        if not has_ans:
            errors.append(f"Q{qnum} in {file_name} is missing Answer Check (- 정답 체크:).")
        if not has_story:
            errors.append(f"Q{qnum} in {file_name} is missing Story Script (- 지문:).")
            
        # Verify mapped asset image exists
        img_name = img_map.get(str(qnum), f"q{qnum}.png")
        if assets_dir:
            img_path = assets_dir / img_name
            fallback_img = assets_dir / f"q{qnum}.png"
            if not img_path.exists() and not fallback_img.exists():
                errors.append(f"Q{qnum} in {file_name}: Mapped asset image '{img_name}' not found at {assets_dir}")
                
    # Verify sequential questions
    if len(q_nums) != 20:
        errors.append(f"Storyboard {file_name} does not contain exactly 20 questions (found {len(q_nums)}).")
    else:
        for idx, qnum in enumerate(sorted(q_nums), 1):
            if qnum != idx:
                errors.append(f"Question order is broken in {file_name}: expected Q{idx}, got Q{qnum}")
                
    # 3. Check EVENT1 ~ EVENT4
    event_parts = content.split('## EVENT')
    event_nums = []
    next_stages = []
    
    for part in event_parts[1:]:
        lines = part.strip().split('\n')
        evnum_str = lines[0].strip()
        if not evnum_str.isdigit():
            continue
        evnum = int(evnum_str)
        event_nums.append(evnum)
        
        for line in lines[1:]:
            line_str = line.strip()
            if line_str.startswith('- 다음 스테이지:'):
                next_stage = line_str.replace('- 다음 스테이지:', '').strip()
                next_stages.append((evnum, next_stage))
                
    # Verify events count
    if len(event_nums) != 4:
        errors.append(f"Storyboard {file_name} does not contain exactly 4 events (found {len(event_nums)}).")
        
    # Verify transitions (Dead Scene Check)
    for evnum, next_stage in next_stages:
        # Valid next stages are: panel_q6, panel_q11, panel_q16, outro
        valid_stages = ["panel_q6", "panel_q11", "panel_q16", "outro"]
        if next_stage not in valid_stages:
            errors.append(f"Event {evnum} in {file_name} has invalid transition target '{next_stage}'.")
            
    return errors

def main():
    project_root = Path(__file__).resolve().parents[3]
    storyboard_root = project_root / "data" / "storyboards"
    
    grades = ["grade1", "grade2", "grade3"]
    total_errors = []
    
    print("=== Story Static Analyzer ===")
    
    storyboard_files = []
    for g in grades:
        grade_dir = storyboard_root / g
        if grade_dir.exists():
            for f in os.listdir(grade_dir):
                if f.endswith("_storyboard.md"):
                    storyboard_files.append(grade_dir / f)
                    
    print(f"Found {len(storyboard_files)} active storyboards for validation.")
    
    for sb_file in sorted(storyboard_files):
        print(f"Analyzing: {sb_file.name}...")
        errors = validate_storyboard(sb_file, project_root)
        if errors:
            print(f"   [FAIL] {len(errors)} anomalies detected:")
            for err in errors:
                print(f"      - {err}")
            total_errors.extend(errors)
        else:
            print("   [PASS] Statically verified.")
            
    print("\n=== Validation Results ===")
    if total_errors:
        print(f"Total Validation Anomalies: {len(total_errors)}")
        sys.exit(1)
    else:
        print("[+] SUCCESS: All active storyboards passed pipeline verification!")
        sys.exit(0)

if __name__ == "__main__":
    main()
