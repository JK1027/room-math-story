import os
import sys
import re
import time
import json
import argparse
from pathlib import Path

# --- Central Configs Loading ---
_cur = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(os.path.dirname(os.path.dirname(_cur)))
if _root not in sys.path:
    sys.path.append(_root)
from scripts.config import paths
from scripts.config.constants import SUPPORTED_GRADES

# 바이블 위반 금지어 (AI 관련 메타 단어 및 비속어 등)
BANNED_KEYWORDS = ["chatgpt", "gpt", "인공지능", "openai", "bard", "gemini"]

def load_metadata_yaml(filepath):
    """Safe regex-based YAML parser for grade metadata.yaml files."""
    data = {"units": {}}
    if not os.path.exists(filepath):
        return data
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple regex parser for our metadata format
    units_block = re.search(r'units:\n([\s\S]*)', content)
    if units_block:
        units_content = units_block.group(1)
        # Split by unit keys (e.g. m1_01:)
        unit_blocks = re.findall(r'  (\w+):\n([\s\S]*?)(?=\n  \w+:|$)', units_content)
        for u_id, u_body in unit_blocks:
            unit_data = {"characters": {}}
            for line in u_body.split('\n'):
                line = line.strip()
                if line.startswith('title:'):
                    unit_data["title"] = line.replace('title:', '').strip().strip('"\'')
                elif line.startswith('builder:'):
                    unit_data["builder"] = line.replace('builder:', '').strip().strip('"\'')
                elif line.startswith('storyboard:'):
                    unit_data["storyboard"] = line.replace('storyboard:', '').strip().strip('"\'')
                elif line.startswith('hero:'):
                    unit_data["characters"]["hero"] = line.replace('hero:', '').strip().strip('"\'')
                elif line.startswith('helper:'):
                    unit_data["characters"]["helper"] = line.replace('helper:', '').strip().strip('"\'')
                elif line.startswith('villain:'):
                    unit_data["characters"]["villain"] = line.replace('villain:', '').strip().strip('"\'')
            data["units"][u_id] = unit_data
            
    return data

def check_bible_violations(text, file_name):
    """Checks for banned keywords in script text."""
    violations = []
    text_lower = text.lower()
    for kw in BANNED_KEYWORDS:
        if kw in text_lower:
            violations.append(f"Banned keyword '{kw}' found in {file_name}")
    return violations

def validate_storyboard(file_path, metadata=None):
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
    
    # Metadata cross-verification
    unit_id = file_name.replace("_storyboard.md", "")
    if metadata and "units" in metadata and unit_id in metadata["units"]:
        unit_meta = metadata["units"][unit_id]
        expected_helper = unit_meta.get("characters", {}).get("helper")
        expected_villain = unit_meta.get("characters", {}).get("villain")
        
        if expected_helper and expected_helper not in content:
            errors.append(f"Helper character '{expected_helper}' defined in metadata was not found in storyboard {file_name}")
        if expected_villain and expected_villain not in content:
            errors.append(f"Villain character '{expected_villain}' defined in metadata was not found in storyboard {file_name}")
    
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
    assets_root = paths.APPS_DIR / "assets"
    
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
    start_time = time.time()
    
    parser = argparse.ArgumentParser(description="Storyboard Static Analyzer")
    parser.add_argument('--json', action='store_true', help='Output results as a structured JSON string')
    args = parser.parse_args()
    
    storyboard_root = paths.STORYBOARDS_DIR
    total_errors = []
    
    # Load grade metadata dictionaries
    grade_metadata = {}
    for g in SUPPORTED_GRADES:
        meta_file = paths.story_dir(g) / "metadata.yaml"
        grade_metadata[g] = load_metadata_yaml(meta_file)
        
    storyboard_files = []
    for g in SUPPORTED_GRADES:
        grade_dir = storyboard_root / g
        if grade_dir.exists():
            for f in os.listdir(grade_dir):
                if f.endswith("_storyboard.md"):
                    storyboard_files.append((g, grade_dir / f))
                    
    results = []
    for g, sb_file in sorted(storyboard_files, key=lambda x: x[1].name):
        meta = grade_metadata.get(g)
        errors = validate_storyboard(sb_file, meta)
        if errors:
            total_errors.extend(errors)
            results.append({
                "file": sb_file.name,
                "status": "FAIL",
                "errors": len(errors)
            })
        else:
            results.append({
                "file": sb_file.name,
                "status": "PASS",
                "errors": 0
            })
            
    duration = f"{time.time() - start_time:.2f}s"
    
    if args.json:
        output_data = {
            "status": "FAIL" if total_errors else "PASS",
            "errors": len(total_errors),
            "warnings": 0,
            "duration": duration,
            "details": results
        }
        print(json.dumps(output_data, ensure_ascii=False, indent=2))
        sys.exit(1 if total_errors else 0)
        
    # Human-readable output fallback
    print("=== Story Static Analyzer ===")
    print(f"Found {len(storyboard_files)} active storyboards for validation.")
    for res in results:
        print(f"Analyzing: {res['file']}...")
        if res['errors'] > 0:
            print(f"   [FAIL] {res['errors']} anomalies detected.")
        else:
            print("   [PASS] Statically verified.")
            
    print("\n=== Validation Results ===")
    if total_errors:
        print(f"Total Validation Anomalies: {len(total_errors)}")
        for idx, err in enumerate(total_errors, 1):
            print(f"  {idx}. {err}")
        sys.exit(1)
    else:
        print(f"[+] SUCCESS: All active storyboards passed pipeline verification! (Duration: {duration})")
        sys.exit(0)

if __name__ == "__main__":
    main()
