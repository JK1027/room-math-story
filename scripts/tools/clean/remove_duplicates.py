import os
import sys
import hashlib
import shutil
import argparse
from pathlib import Path

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def main():
    parser = argparse.ArgumentParser(description="Remove duplicate script markdown files and archive old txt drafts.")
    parser.add_argument('--dry-run', action='store_true', help='Show duplicate files and changes without applying them.')
    parser.add_argument('--apply', action='store_true', help='Apply the file deletion and migration changes.')
    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        print("Error: You must specify either --dry-run or --apply")
        parser.print_help()
        sys.exit(1)

    # --- Central Configs Loading ---
    import sys
    _cur = os.path.dirname(os.path.abspath(__file__))
    _root = os.path.dirname(os.path.dirname(os.path.dirname(_cur)))
    if _root not in sys.path:
        sys.path.append(_root)
    from scripts.config import paths
    from scripts.config.constants import SUPPORTED_GRADES

    project_root = paths.ROOT_DIR
    archive_dir = paths.ARCHIVE_DIR / "releases"
    legacy_draft_dir = paths.LEGACY_DRAFTS_DIR
    stories_dir = paths.STORIES_DIR

    grades = SUPPORTED_GRADES

    if not archive_dir.exists():
        print(f"Archive directory not found: {archive_dir}")
        sys.exit(0)

    import re

    # 1. 중복 마크다운 파일 검출 및 해시 비교
    files_to_delete = []
    files_with_mismatch = []
    txt_files_to_move = []

    for item in os.listdir(archive_dir):
        item_path = archive_dir / item
        if not item_path.is_file():
            continue

        if item.endswith("_script.md") or item.endswith(".md"):
            # prefix 매칭 (예: m1_04_atlantis_script.md -> m1_04)
            prefix_match = re.match(r'^(m\d+_\d+)', item)
            prefix = prefix_match.group(1) if prefix_match else None
            
            original_found = False
            if prefix:
                for grade in grades:
                    grade_folder = stories_dir / grade
                    if grade_folder.exists():
                        for stories_item in os.listdir(grade_folder):
                            if stories_item.startswith(prefix) and stories_item.endswith(".md"):
                                orig_path = grade_folder / stories_item
                                original_found = True
                                archive_hash = calculate_md5(item_path)
                                orig_hash = calculate_md5(orig_path)
                                if archive_hash == orig_hash:
                                    files_to_delete.append((item_path, orig_path, archive_hash))
                                else:
                                    files_with_mismatch.append((item_path, orig_path, archive_hash, orig_hash))
                                break
                    if original_found:
                        break
            if not original_found:
                print(f"[-] Original not found for archive file: {item}. Keeping this file.")
        
        elif item.endswith(".txt"):
            txt_files_to_move.append(item_path)

    # 결과 보고
    print("=== SUMMARY OF DUPLICATE DETECTOR ===")
    print(f"1. Verified duplicates (to be deleted): {len(files_to_delete)}")
    for arch, orig, h in files_to_delete:
        print(f"   [DELETE candidate] {arch.name} (MD5: {h})")
        print(f"      Matched with: {orig}")

    if files_with_mismatch:
        print(f"\n[WARNING] Found mismatching hashes: {len(files_with_mismatch)}")
        for arch, orig, ah, oh in files_with_mismatch:
            print(f"   [MISMATCH] {arch.name} (Archive Hash: {ah}) vs Original (Hash: {oh})")
            print(f"      Original path: {orig}")
            print("      *These files will NOT be deleted for safety.*")

    print(f"\n2. Old drafts (to be moved to legacy/draft_stories/): {len(txt_files_to_move)}")
    for txt in txt_files_to_move:
        print(f"   [MOVE candidate] {txt.name} -> {legacy_draft_dir / txt.name}")

    if args.dry_run:
        print("\n*** DRY-RUN COMPLETE. No changes were applied. Use --apply to execute. ***")
        return

    # Apply 수행
    print("\n=== APPLYING CHANGES ===")
    
    # legacy 폴더 생성
    if txt_files_to_move:
        legacy_draft_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created legacy directory: {legacy_draft_dir}")

    # 파일 삭제
    deleted_count = 0
    for arch, _, _ in files_to_delete:
        try:
            arch.unlink()
            print(f"Deleted duplicate: {arch.name}")
            deleted_count += 1
        except Exception as e:
            print(f"Error deleting {arch.name}: {e}")

    # 파일 이동
    moved_count = 0
    for txt in txt_files_to_move:
        try:
            shutil.move(str(txt), str(legacy_draft_dir / txt.name))
            print(f"Moved draft: {txt.name}")
            moved_count += 1
        except Exception as e:
            print(f"Error moving {txt.name}: {e}")

    print(f"\nSuccessfully deleted {deleted_count} files and moved {moved_count} files.")

if __name__ == "__main__":
    main()
