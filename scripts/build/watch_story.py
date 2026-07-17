"""
watch_story.py - 실시간 대본집 파일 감시 핫리로드 도구

stories/ 및 quiz_data/ 폴더 내의 .md 및 .yaml 파일 변경을 감시합니다.
수정 저장이 감지되면 build_story.build_unit(unit_id) 를 인-프로세스로 즉시 호출합니다.
(subprocess 없이 직접 함수 호출 — 단일 로그, 최소 오버헤드)

사용법:
    python scripts/build/watch_story.py
    (종료: Ctrl+C)
"""
import os
import sys
import re
import time

# --- Central Configs Loading ---
_cur = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(os.path.dirname(_cur))
if _root not in sys.path:
    sys.path.append(_root)

from scripts.config import paths
from scripts.build.build_story import build_unit  # 직접 함수 임포트

# 감시할 경로 목록
WATCH_DIRS = [
    paths.STORIES_DIR,
    paths.ROOT_DIR / "quiz_data",
]


def get_file_timestamps() -> dict:
    """감시 대상 폴더 내 .md 및 .yaml 파일들의 최근 수정 시간 맵을 반환합니다."""
    timestamps = {}
    for wdir in WATCH_DIRS:
        if not wdir.exists():
            continue
        for root, _, files in os.walk(wdir):
            for f in files:
                if f.endswith(".md") or f.endswith(".yaml"):
                    fpath = os.path.join(root, f)
                    try:
                        timestamps[fpath] = os.path.getmtime(fpath)
                    except OSError:
                        pass
    return timestamps


def detect_unit_from_path(filepath: str) -> str | None:
    """수정된 파일의 경로명으로부터 단원 코드(예: m1_02)를 추출합니다."""
    fname = os.path.basename(filepath)
    match = re.search(r'(m\d+_\d+)', fname)
    return match.group(1) if match else None


def main():
    print("=" * 52)
    print("  수학 방탈출 대본/퀴즈 핫리로드 Watcher 기동")
    print("  (stories/ 및 quiz_data/ 수정 저장 시 자동 빌드)")
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
                # 변경된 파일에서 단원 코드 추출 (중복 제거)
                units_to_build = set(
                    u for f in changed_files
                    if (u := detect_unit_from_path(f)) is not None
                )

                for unit_id in sorted(units_to_build):
                    print(f"\n⚡ [WATCH] 변경 감지 → {unit_id.upper()} 단원 자동 리빌드 개시!")
                    success = build_unit(unit_id)   # 직접 함수 호출 (in-process)
                    if success:
                        sys.stdout.write('\a')       # 완료 알림음
                        sys.stdout.flush()
                    else:
                        print(f"  ⚠️  [{unit_id.upper()}] 빌드 실패 — 대본 또는 YAML 내용을 확인하세요.")

                last_timestamps = current_timestamps

    except KeyboardInterrupt:
        print("\n[Watcher] 감시가 안전하게 종료되었습니다.")


if __name__ == "__main__":
    main()
