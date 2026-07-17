import os
import sys
import re
import time
import json
import argparse
import yaml
import unicodedata
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

def read_file_safe(filepath):
    """
    파일의 인코딩(utf-8-sig, utf-8, cp949)을 판별하여 깨짐 없이 온전하게 로드합니다.
    """
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            content = f.read()
            if "units" in content or "질문" in content or "지문" in content or "이미지" in content:
                return content.replace('\r\n', '\n')
    except UnicodeDecodeError:
        pass

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if "units" in content or "질문" in content or "지문" in content or "이미지" in content:
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

def load_metadata_yaml(filepath):
    """Safe regex-based YAML parser for grade metadata.yaml files."""
    data = {"units": {}}
    if not os.path.exists(filepath):
        return data
    content = read_file_safe(filepath)
    
    units_block = re.search(r'units:\n([\s\S]*)', content)
    if units_block:
        units_content = units_block.group(1)
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

def validate_quiz_data_schema(unit, filepath):
    """
    quiz_data/*.yaml 파일이 정해진 스키마 규칙을 충족하는지 강제 정적 심사합니다.
    """
    errors = []
    if not os.path.exists(filepath):
        errors.append(f"Quiz metadata file not found for {unit} at {filepath}")
        return errors
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        errors.append(f"YAML parsing error in {unit}.yaml: {e}")
        return errors
        
    if not isinstance(data, dict):
        errors.append(f"Invalid YAML structure in {unit}.yaml. Must be an object.")
        return errors
        
    # 필수 최상위 키 검증
    for required_key in ["image_mapping", "questions", "events"]:
        if required_key not in data:
            errors.append(f"Missing required key '{required_key}' in {unit}.yaml")
            
    # 1. image_mapping 검증
    img_map = data.get("image_mapping", {})
    if not isinstance(img_map, dict):
        errors.append(f"'image_mapping' must be a dictionary in {unit}.yaml")
    else:
        for k in ["intro", "outro", "event1", "event2", "event3", "event4"]:
            if k not in img_map:
                errors.append(f"Missing image mapping key '{k}' in {unit}.yaml")
        for i in range(1, 21):
            qkey = f"q{i}"
            if qkey not in img_map:
                errors.append(f"Missing image mapping key '{qkey}' in {unit}.yaml")
                
    # 2. questions 검증
    qs = data.get("questions", {})
    if not isinstance(qs, dict):
        errors.append(f"'questions' must be a dictionary in {unit}.yaml")
    else:
        for i in range(1, 21):
            qkey = f"q{i}"
            if qkey not in qs:
                errors.append(f"Missing question definition for '{qkey}' in {unit}.yaml")
            else:
                qmeta = qs[qkey]
                for required_qfield in ["title", "qtext", "hint", "ans_check"]:
                    if required_qfield not in qmeta or not str(qmeta[required_qfield]).strip():
                        errors.append(f"Question '{qkey}' in {unit}.yaml is missing required field '{required_qfield}'")
                        
    # 3. events 검증
    evs = data.get("events", {})
    if not isinstance(evs, dict):
        errors.append(f"'events' must be a dictionary in {unit}.yaml")
    else:
        for i in range(1, 5):
            ekey = f"event{i}"
            if ekey not in evs:
                errors.append(f"Missing event definition for '{ekey}' in {unit}.yaml")
            else:
                emeta = evs[ekey]
                for required_efield in ["title", "btn_text", "next_stage", "progress"]:
                    if required_efield not in emeta:
                        errors.append(f"Event '{ekey}' in {unit}.yaml is missing required field '{required_efield}'")
                        
    return errors



def validate_storyboard(file_path, metadata=None):
    """
    Statically analyzes a single storyboard markdown file.
    """
    errors = []
    file_name = os.path.basename(file_path)
    
    content = read_file_safe(file_path)
    content = unicodedata.normalize('NFC', content)
        
    violations = check_bible_violations(content, file_name)
    errors.extend(violations)
    
    unit_id = file_name.replace("_storyboard.md", "")
    if metadata and "units" in metadata and unit_id in metadata["units"]:
        unit_meta = metadata["units"][unit_id]
        expected_helper = unit_meta.get("characters", {}).get("helper")
        expected_villain = unit_meta.get("characters", {}).get("villain")
        
        if expected_helper:
            expected_helper = unicodedata.normalize('NFC', expected_helper)
            if expected_helper not in content:
                errors.append(f"Helper character '{expected_helper}' defined in metadata was not found in storyboard {file_name}")
        if expected_villain:
            expected_villain = unicodedata.normalize('NFC', expected_villain)
            if expected_villain not in content:
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
                    
    # Check images existence
    assets_folder = None
    for dname in os.listdir(paths.APPS_DIR / "assets"):
        if dname.startswith(unit_id) and os.path.isdir(paths.APPS_DIR / "assets" / dname):
            assets_folder = dname
            break
            
    if assets_folder:
        for k, v in img_map.items():
            img_path = paths.APPS_DIR / "assets" / assets_folder / v
            if not img_path.exists():
                errors.append(f"Target asset '{v}' for key '{k}' does not exist at {img_path}")
                
    # 2. Parse Q1 to Q20 definitions
    q_matches = re.findall(r'## Q(\d+)', content)
    q_nums = [int(x) for x in q_matches]
    if q_nums != list(range(1, 21)):
        errors.append(f"Storyboard {file_name} does not contain sequential questions Q1 to Q20. Found: {q_nums}")
        
    # Check each question metadata
    q_blocks = content.split('## Q')
    for q_block in q_blocks[1:]:
        lines = q_block.strip().split('\n')
        qnum_str = lines[0].strip()
        if not qnum_str.isdigit():
            continue
        qnum = int(qnum_str)
        
        required_fields = ["제목:", "이미지:", "질문:", "힌트:", "정답 체크:", "지문:"]
        for fld in required_fields:
            if fld not in q_block:
                errors.append(f"Question Q{qnum} in {file_name} is missing key field '{fld.replace(':', '')}'.")
                
    # 3. Parse EVENT1 to EVENT4 definitions
    ev_matches = re.findall(r'## EVENT(\d+)', content)
    ev_nums = [int(x) for x in ev_matches]
    if ev_nums != list(range(1, 5)):
        errors.append(f"Storyboard {file_name} does not contain sequential events EVENT1 to EVENT4. Found: {ev_nums}")
        
    ev_blocks = content.split('## EVENT')
    next_stages = []
    for ev_block in ev_blocks[1:]:
        lines = ev_block.strip().split('\n')
        evnum_str = lines[0].strip()
        if not evnum_str.isdigit():
            continue
        evnum = int(evnum_str)
        
        required_fields = ["제목:", "이미지:", "버튼 텍스트:", "다음 스테이지:", "달성도:", "지문:"]
        for fld in required_fields:
            if fld not in ev_block:
                errors.append(f"Event EVENT{evnum} in {file_name} is missing key field '{fld.replace(':', '')}'.")
                
        # Transition check
        ns_match = re.search(r'- 다음 스테이지:\s*(.*)', ev_block)
        if ns_match:
            next_stages.append((evnum, ns_match.group(1).strip()))
        
    # Verify transitions (Dead Scene Check)
    for evnum, next_stage in next_stages:
        valid_stages = ["panel_q6", "panel_q11", "panel_q16", "outro"]
        if next_stage not in valid_stages:
            errors.append(f"Event {evnum} in {file_name} has invalid transition target '{next_stage}'.")
            
    return errors

def validate_for_unit(unit_id: str) -> bool:
    """
    [Programmatic API] 특정 단원의 YAML 스키마 및 Generated 스토리보드를
    정적 심사하여 합격 여부를 반환합니다.

    Args:
        unit_id: 단원 코드 (예: "m1_02")
    Returns:
        True 검증 통과, False 검증 실패
    """
    grade_str = "grade1" if "m1_" in unit_id else ("grade2" if "m2_" in unit_id else "grade3")
    quiz_data_root = paths.ROOT_DIR / "quiz_data"
    storyboard_root = paths.ROOT_DIR / "storyboards" / "generated"

    total_errors = []

    # YAML 스키마 검증
    yaml_path = quiz_data_root / grade_str / f"{unit_id}.yaml"
    if yaml_path.exists():
        yaml_errors = validate_quiz_data_schema(unit_id, yaml_path)
        if yaml_errors:
            total_errors.extend(yaml_errors)
            print(f"  [FAIL] {unit_id}.yaml: {len(yaml_errors)} schema violations.")
        else:
            print(f"  [PASS] {unit_id}.yaml schema compliant.")
    else:
        total_errors.append(f"{unit_id}.yaml not found in quiz_data/{grade_str}")

    # 스토리보드 검증
    sb_path = storyboard_root / grade_str / f"{unit_id}_storyboard.md"
    meta_file = paths.story_dir(grade_str) / "metadata.yaml"
    meta = load_metadata_yaml(str(meta_file))

    if sb_path.exists():
        sb_errors = validate_storyboard(sb_path, meta)
        if sb_errors:
            total_errors.extend(sb_errors)
            print(f"  [FAIL] {unit_id}_storyboard.md: {len(sb_errors)} anomalies.")
        else:
            print(f"  [PASS] {unit_id}_storyboard.md verified.")
    else:
        total_errors.append(f"{unit_id}_storyboard.md not found in storyboards/generated/{grade_str}")

    return len(total_errors) == 0


def main():
    start_time = time.time()

    parser = argparse.ArgumentParser(description="Storyboard & Quiz Static Schema Analyzer")
    parser.add_argument('--json', action='store_true', help='Output results as a structured JSON string')
    parser.add_argument('--unit', type=str, default=None,
                        help='Validate only a single unit (e.g. m1_02). Omit to validate all units.')
    args = parser.parse_args()

    # 단일 유닛 검증 모드
    if args.unit:
        print(f"\n=== Validating Unit: {args.unit} ===")
        ok = validate_for_unit(args.unit)
        print(f"\n=== Validation Results ===")
        if ok:
            print(f"[+] SUCCESS: {args.unit} passed all checks.")
            sys.exit(0)
        else:
            print(f"[-] FAILED: {args.unit} has validation errors.")
            sys.exit(1)
    
    storyboard_root = paths.ROOT_DIR / "storyboards" / "generated"
    if not storyboard_root.exists():
        storyboard_root = paths.STORYBOARDS_DIR
    quiz_data_root = paths.ROOT_DIR / "quiz_data"
    total_errors = []
    
    # 1. Pre-validate YAML Files (Quiz Data Schema Audit)
    print("=== Quiz Data Schema Verification ===")
    yaml_count = 0
    for g in SUPPORTED_GRADES:
        yaml_grade_dir = quiz_data_root / g
        if yaml_grade_dir.exists():
            for f in os.listdir(yaml_grade_dir):
                if f.endswith(".yaml"):
                    unit_id = f.replace(".yaml", "")
                    print(f"Auditing schema for: {f}...")
                    yaml_errors = validate_quiz_data_schema(unit_id, yaml_grade_dir / f)
                    if yaml_errors:
                        total_errors.extend(yaml_errors)
                        print(f"   [FAIL] {len(yaml_errors)} schema violations found.")
                    else:
                        print("   [PASS] Schema compliant.")
                    yaml_count += 1
    
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
    print("\n=== Generated Storyboard Verification ===")
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
            print(f"Analyzing: {sb_file.name}... [FAIL] {len(errors)} anomalies.")
        else:
            results.append({
                "file": sb_file.name,
                "status": "PASS",
                "errors": 0
            })
            print(f"Analyzing: {sb_file.name}... [PASS]")
            
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
        
    print("\n=== Validation Results ===")
    if total_errors:
        print(f"Total Validation Anomalies: {len(total_errors)}")
        for idx, err in enumerate(total_errors, 1):
            print(f"  {idx}. {err}")
        sys.exit(1)
    else:
        print(f"[+] SUCCESS: All {yaml_count} YAMLs and storyboards passed verification! (Duration: {duration})")
        sys.exit(0)

if __name__ == "__main__":
    main()
