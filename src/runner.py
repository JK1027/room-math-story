import os
import sys
import time
import json
from src.parser import parse_chapter
from src.story_validator import validate_chapter_rules
from src.storybook_builder import StorybookBuilder
from src.game_builder import GameBuilder
from scripts.config import paths

def write_json_report(report_data: dict):
    """최종 빌드 분석 통계서를 build/report.json 에 기록합니다."""
    build_dir = paths.ROOT_DIR / "build"
    build_dir.mkdir(exist_ok=True)
    report_file = build_dir / "report.json"
    
    try:
        with open(report_file, 'w', encoding='utf-8') as rf:
            json.dump(report_data, rf, ensure_ascii=False, indent=2)
        print(f"\n[+] Build report generated successfully: {report_file.name}")
    except Exception as e:
        print(f"[-] Failed to generate build report: {e}", file=sys.stderr)

def run_pipeline(grade_str: str, unit_code: str, build_storybook_flag: bool = True, build_game_flag: bool = False) -> bool:
    """
    [PipelineRunner 코어] 단일 단원(예: m1_02)에 대해 
    Parse → Validate → Build(Storybook/Game) E2E 실행을 수행하는 유일 게이트웨이입니다.
    """
    start_time = time.time()
    chapter_path = paths.story_path(grade_str, unit_code)
    chapter_file_name = chapter_path.name
    
    print(f"\n>>> Running Pipeline for {unit_code.upper()} ({chapter_file_name})")
    
    # ─── 1. PARSE ──────────────────────────────────────
    print("  [1/3] Parsing Chapter Source...")
    parse_result = parse_chapter(str(chapter_path))
    
    if not parse_result.ok:
        print("  [-] Parsing FAILED with following errors:", file=sys.stderr)
        for err in parse_result.errors:
            print(f"    - {err}", file=sys.stderr)
        return False
        
    chapter = parse_result.chapter
    print(f"  [OK] Heading-based DSL Chapter '{chapter.title}' parsed.")
    
    # ─── 2. VALIDATE (Gatekeeper) ────────────────────────
    print("  [2/3] Auditing Content Rules & Assets...")
    val_errors, val_warnings = validate_chapter_rules(chapter, grade_str, unit_code)
    
    if val_warnings:
        print("  [Warning] Rule alerts:")
        for warn in val_warnings:
            print(f"    - {warn}")
            
    if val_errors:
        print("  ❌ [VALIDATION GATE BLOCKED] Build aborted due to validation errors:", file=sys.stderr)
        for err in val_errors:
            print(f"    - {err}", file=sys.stderr)
        return False
        
    print("  [OK] Validation passed. Proceeding to compilation...")
    
    # ─── 3. BUILD (Base Builders ABC Execution) ──────────
    built_storybook = False
    built_game = False
    
    if build_storybook_flag:
        print("  [3/3] Building Storybook Viewer...")
        s_builder = StorybookBuilder()
        built_storybook = s_builder.build(chapter, grade_str, unit_code)
        if not built_storybook:
            return False
            
    if build_game_flag:
        print("  [3/3] Building Escape Room Game App...")
        g_builder = GameBuilder()
        built_game = g_builder.build(chapter, grade_str, unit_code)
        if not built_game:
            return False
            
    elapsed = f"{time.time() - start_time:.2f}s"
    print(f">>> [SUCCESS] {unit_code.upper()} Pipeline finished successfully in {elapsed}!")
    
    # 리포트 발행
    report_data = {
        "status": "SUCCESS",
        "unit": unit_code,
        "grade": grade_str,
        "title": chapter.title,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "duration": elapsed,
        "storybook_viewer_built": built_storybook,
        "game_app_built": built_game,
        "anomalies": {
            "warnings_count": len(val_warnings),
            "warnings": val_warnings
        }
    }
    write_json_report(report_data)
    return True
