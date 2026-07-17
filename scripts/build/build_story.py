"""
build_story.py - 단일 책임 오케스트레이터 (Sole Orchestrator)

사용법:
    python build_story.py                  # 전체 23개 단원 E2E 빌드
    python build_story.py --unit m1_02     # 특정 단원만 E2E 빌드

외부 프로그램 연동용 API:
    from scripts.build.build_story import build_unit, build_all
    build_unit("m1_02")
    build_all()
"""
import os
import sys
import subprocess
import glob
import time
import yaml
import argparse
from pathlib import Path

# --- Central Configs Loading ---
_cur = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(os.path.dirname(_cur))
if _root not in sys.path:
    sys.path.append(_root)
from scripts.config import paths
from scripts.config.constants import SUPPORTED_GRADES

# ====================================================
# 빌더 파일명 → 단원 코드 매핑 테이블
# ====================================================
BUILDER_UNIT_MAP = {
    "update_app_01.py": "m1_01",
    "update_app_02.py": "m1_02",
    "update_app_03.py": "m1_03",
    "update_app_04.py": "m1_04",
    "update_app_05.py": "m1_05",
    "update_app_06.py": "m1_06",
    "update_app_07.py": "m1_07",
    "update_app_08.py": "m1_08",
    "update_app_m2_01.py": "m2_01",
    "update_app_m2_02.py": "m2_02",
    "update_app_m2_03.py": "m2_03",
    "update_app_m2_04.py": "m2_04",
    "update_app_m2_05.py": "m2_05",
    "update_app_m2_06.py": "m2_06",
    "update_app_m2_07.py": "m2_07",
    "update_app_m2_08.py": "m2_08",
    "update_app_m3_01.py": "m3_01",
    "update_app_m3_02.py": "m3_02",
    "update_app_m3_03.py": "m3_03",
    "update_app_m3_04.py": "m3_04",
    "update_app_m3_05.py": "m3_05",
    "update_app_m3_06.py": "m3_06",
    "update_app_m3_07.py": "m3_07",
}
UNIT_BUILDER_MAP = {v: k for k, v in BUILDER_UNIT_MAP.items()}

# ====================================================
# 내부 유틸: subprocess 실행기
# ====================================================
def _run_script(script_path, args=None):
    """Runs a Python script and prints its output. Returns True if successful."""
    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(f"[stderr] {result.stderr.strip()}", file=sys.stderr)
    return result.returncode == 0


def _write_report(report_data: dict):
    """빌드 결과를 .build/build_report.yaml 에 기록합니다."""
    build_dir = paths.ROOT_DIR / ".build"
    build_dir.mkdir(exist_ok=True)
    report_path = build_dir / "build_report.yaml"
    try:
        with open(report_path, 'w', encoding='utf-8') as rf:
            yaml.dump(report_data, rf, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print(f"\n[+] Build report written to: {report_path}")
    except Exception as e:
        print(f"[-] Failed to write build report: {e}", file=sys.stderr)


# ====================================================
# [Programmatic API] build_unit(unit_id)
# ====================================================
def build_unit(unit_id: str) -> bool:
    """
    [Programmatic API] 특정 단원의 E2E 빌드 파이프라인을 실행합니다.
    파이프라인 순서: Generate → Validate (실패 시 중단) → HTML → PDF

    Args:
        unit_id: 단원 코드 (예: "m1_02")
    Returns:
        True 전체 성공, False 하나라도 실패 또는 Validation Gate 차단
    """
    start_time = time.time()
    print(f"\n{'='*52}")
    print(f"  [BUILD] 단원 {unit_id.upper()} E2E 파이프라인 가동")
    print(f"{'='*52}")

    generator_script = paths.ROOT_DIR / "scripts" / "tools" / "story" / "storyboard_generator.py"
    validate_script   = paths.ROOT_DIR / "scripts" / "tools" / "story" / "validate_story.py"
    pdf_script        = paths.ROOT_DIR / "scripts" / "build"  / "build_pdf.py"
    builders_dir      = paths.ROOT_DIR / "scripts" / "builders"

    # ─── Step 1: Generate ────────────────────────────────
    print(f"\n  [1/4] Generate: {unit_id}_storyboard.md 합성 중...")
    ok = _run_script(generator_script, args=['--unit', unit_id])
    if not ok:
        print(f"  [-] Generate FAILED for {unit_id}. Aborting.", file=sys.stderr)
        return False

    # ─── Step 2: Validate (Gatekeeper) ───────────────────
    print(f"\n  [2/4] Validate: 스키마 및 스토리보드 정적 심사 중...")
    ok = _run_script(validate_script, args=['--unit', unit_id])
    if not ok:
        print(f"\n  [BLOCKED] [VALIDATION GATE BLOCKED] {unit_id} 검증 실패 — HTML/PDF 빌드 중단.", file=sys.stderr)
        return False
    print(f"  [OK] Validation passed -- proceeding to next step.")

    # ─── Step 3: HTML Builder ────────────────────────────
    builder_filename = UNIT_BUILDER_MAP.get(unit_id)
    if builder_filename:
        builder_path = builders_dir / builder_filename
        print(f"\n  [3/4] HTML Build: {builder_filename} 실행 중...")
        ok = _run_script(builder_path)
        if not ok:
            print(f"  [-] HTML build FAILED for {unit_id}.", file=sys.stderr)
            return False
    else:
        print(f"\n  [3/4] HTML Build: {unit_id}에 해당하는 빌더 없음 — 스킵.")

    # ─── Step 4: PDF Builder ─────────────────────────────
    print(f"\n  [4/4] PDF Build: {unit_id}_storyboard.pdf 컴파일 중...")
    ok = _run_script(pdf_script, args=['--unit', unit_id])
    if not ok:
        print(f"  [-] PDF build FAILED for {unit_id}.", file=sys.stderr)
        return False

    elapsed = f"{time.time() - start_time:.2f}s"
    print(f"\n  [SUCCESS] [{unit_id.upper()}] E2E 빌드 완료! (소요: {elapsed})")
    return True


# ====================================================
# [Programmatic API] build_all()
# ====================================================
def build_all() -> bool:
    """
    [Programmatic API] 전체 23개 단원에 대해 E2E 빌드 파이프라인을 실행합니다.
    단원마다 파이프라인이 독립 실행되며 실패 단원도 개별 추적합니다.

    Returns:
        True 전체 성공, False 하나 이상 실패
    """
    start_time = time.time()

    print("====================================================")
    print("|   수학방탈출 스토리 제작 & 빌드 파이프라인 가동          |")
    print("====================================================")

    # 1. 전체 스키마 사전 검증 (생성 전 사전 차단)
    validate_script = paths.ROOT_DIR / "scripts" / "tools" / "story" / "validate_story.py"
    print("\n[Pre-flight] 전체 YAML 스키마 사전 검증 중...")
    if validate_script.exists():
        ok = _run_script(validate_script)
        if not ok:
            print("[-] Pre-flight validation FAILED. Aborting entire build.", file=sys.stderr)
            _write_report({
                "build_status": "FAILED",
                "reason": "Pre-flight validation failed",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            })
            return False

    all_units = sorted(BUILDER_UNIT_MAP.values())
    success_units = []
    failed_units = []

    for unit_id in all_units:
        ok = build_unit(unit_id)
        if ok:
            success_units.append(unit_id)
        else:
            failed_units.append(unit_id)

    build_time = f"{time.time() - start_time:.2f}s"

    print("\n====================================================")
    print(f"   전체 빌드 완료! (소요: {build_time})")
    print(f"   성공: {len(success_units)}/{len(all_units)} 단원")
    if failed_units:
        print(f"   실패: {', '.join(failed_units)}")
    print("====================================================")

    # Build Report 생성
    _write_report({
        "build_status": "SUCCESS" if not failed_units else "PARTIAL_FAILURE",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "build_time": build_time,
        "metrics": {
            "total_units": len(all_units),
            "success": len(success_units),
            "failed": len(failed_units),
        },
        "failed_units": failed_units,
        "schema_version": "1.1",
    })

    return len(failed_units) == 0


# ====================================================
# CLI Entry Point (사람을 위한 인터페이스)
# ====================================================
def main():
    parser = argparse.ArgumentParser(
        description="수학 방탈출 빌드 오케스트레이터 (Sole Orchestrator)\n"
                    "Generate → Validate → HTML → PDF 순으로 파이프라인을 실행합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--unit', type=str, default=None,
        help='특정 단원만 빌드 (예: m1_02). 생략 시 전체 23개 단원을 빌드합니다.'
    )
    args = parser.parse_args()

    if args.unit:
        ok = build_unit(args.unit)
        sys.exit(0 if ok else 1)
    else:
        ok = build_all()
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
