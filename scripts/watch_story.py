"""
watch_story.py - 단일 원천 대본(chapterXX.md) 실시간 수정 감시 핫리로드 뷰어 연동
"""
import os
import sys
import re
import time

# --- Central Configs Loading ---
_cur = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(_cur)
if _root not in sys.path:
    sys.path.append(_root)
from scripts.config import paths
from src.runner import run_pipeline

WATCH_DIRS = [
    paths.STORIES_DIR
]

def get_file_timestamps() -> dict:
    """감시 폴더 내 chapterXX.md 마크다운 파일들의 최근 수정 시간 맵을 만듭니다."""
    timestamps = {}
    for wdir in WATCH_DIRS:
        if not wdir.exists():
            continue
        for root, _, files in os.walk(wdir):
            for f in files:
                if f.startswith("chapter") and f.endswith(".md"):
                    fpath = os.path.join(root, f)
                    try:
                        timestamps[fpath] = os.path.getmtime(fpath)
                    except OSError:
                        pass
    return timestamps

def detect_unit_and_grade_from_path(filepath: str) -> tuple:
    """수정된 파일의 경로명으로부터 단원 번호 및 학년을 매핑합니다."""
    # stories/grade1/chapter02.md -> grade1, m1_02
    parts = Path(filepath).parts
    grade_str = "grade1"
    for p in parts:
        if p in ["grade1", "grade2", "grade3"]:
            grade_str = p
            break
            
    fname = os.path.basename(filepath)
    match = re.search(r'chapter(\d+)', fname)
    if match:
        num_str = match.group(1)
        grade_num = grade_str[-1] # grade1 -> 1
        return grade_str, f"m{grade_num}_{num_str}"
        
    return None, None

from pathlib import Path

def main():
    print("=" * 52)
    print("  수학 방탈출 SSoT (chapterXX.md) 실시간 Watcher 기동")
    print("  (스토리 수정 저장 즉시 검토용 Storybook Viewer 자동 갱신)")
    print("=" * 52)
    print("감시를 시작합니다... (종료하려면 Ctrl+C 입력)\n")
    
    last_timestamps = get_file_timestamps()
    
    try:
        while True:
            time.sleep(1.0)
            current_timestamps = get_file_timestamps()
            
            changed_files = [
                fpath for fpath, mtime in current_timestamps.items()
                if fpath not in last_timestamps or mtime > last_timestamps[fpath]
            ]
            
            if changed_files:
                for fpath in changed_files:
                    grade_str, unit_code = detect_unit_and_grade_from_path(fpath)
                    if grade_str and unit_code:
                        print(f"\n⚡ [WATCH] 수정 감지: {os.path.basename(fpath)} 리빌드 개시!")
                        # PipelineRunner 호출 (Storybook Viewer 전용 빌드)
                        success = run_pipeline(grade_str, unit_code, build_storybook_flag=True, build_game_flag=False)
                        if success:
                            sys.stdout.write('\a') # 리로드 알림 비프
                            sys.stdout.flush()
                        else:
                            print(f"  [Warning] {unit_code.upper()} 뷰어 리빌드 실패. 마크다운의 구조적 에러를 점검해 주십시오.")
                            
                last_timestamps = current_timestamps
                
    except KeyboardInterrupt:
        print("\n[Watcher] 파일 감시 모드가 종료되었습니다.")

if __name__ == "__main__":
    main()
