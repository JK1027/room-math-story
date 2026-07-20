import os
import json
import hashlib
from pathlib import Path
from PIL import Image

# ----------------- 경로 설정 -----------------
import sys
_cur = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(os.path.dirname(os.path.dirname(_cur)))
if _root not in sys.path:
    sys.path.append(_root)
from scripts.config import paths

RAW_ASSETS_DIR = paths.ROOT_DIR / "assets" / "raw_units"
OPTIMIZED_ASSETS_DIR = paths.ROOT_DIR / "assets" / "units"
CACHE_FILE = paths.ROOT_DIR / "scratch" / "asset_cache.json"

MAX_EDGE = 1280

def get_file_hash(file_path):
    """파일의 SHA-256 해시를 연산합니다."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def optimize_image(src_path, dest_path):
    """Pillow를 사용해 이미지를 최적화(RGB 변환, 리사이징 및 압축)합니다."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    with Image.open(src_path) as img:
        # JPEG로 저장하기 위해 RGB 변환 수행 (JPEG는 RGBA 미지원)
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        width, height = img.size
        # 긴 변 기준 리사이징
        if max(width, height) > MAX_EDGE:
            if width > height:
                new_width = MAX_EDGE
                new_height = int((height * MAX_EDGE) / width)
            else:
                new_height = MAX_EDGE
                new_width = int((width * MAX_EDGE) / height)
            
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            print(f"   [Resized] {src_path.name} ({width}x{height} -> {new_width}x{new_height})")
            
        # JPEG 인코딩(품질 80%)을 적용하여 용량을 수십~백여 KB 수준으로 극대화 압축
        img.save(dest_path, format='JPEG', quality=80)

def optimize_all_assets():
    print("Starting asset optimization pipeline...")
    
    # 캐시 로드
    cache = {}
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache = json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load asset cache, starting fresh. Error: {e}")

    new_cache = {}
    processed_count = 0
    skipped_count = 0
    raw_files_relative = set()

    # raw_assets 스캔 및 최적화
    if not RAW_ASSETS_DIR.exists():
        print(f"Error: RAW_ASSETS_DIR does not exist at {RAW_ASSETS_DIR}")
        return

    for root, _, files in os.walk(RAW_ASSETS_DIR):
        for file in files:
            if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            src_path = Path(root) / file
            rel_path = src_path.relative_to(RAW_ASSETS_DIR)
            raw_files_relative.add(str(rel_path).lower())
            
            dest_path = OPTIMIZED_ASSETS_DIR / rel_path
            
            # 해시 계산
            try:
                curr_hash = get_file_hash(src_path)
            except Exception as e:
                print(f"Error reading {src_path}: {e}")
                continue
                
            new_cache[str(rel_path)] = curr_hash
            
            # 변경 여부 검사 (증분 빌드)
            if cache.get(str(rel_path)) == curr_hash and dest_path.exists():
                skipped_count += 1
                continue
                
            # 최적화 수행
            try:
                print(f"Optimizing: {rel_path}...")
                optimize_image(src_path, dest_path)
                processed_count += 1
            except Exception as e:
                print(f"Error optimizing {rel_path}: {e}")

    # 고아 파일(raw에 없는데 optimized에 남아있는 파일) 삭제 동기화
    deleted_count = 0
    if OPTIMIZED_ASSETS_DIR.exists():
        for root, _, files in os.walk(OPTIMIZED_ASSETS_DIR):
            for file in files:
                if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    continue
                dest_path = Path(root) / file
                rel_path = dest_path.relative_to(OPTIMIZED_ASSETS_DIR)
                
                # raw_assets에 해당 상대경로 파일이 없으면 삭제
                if str(rel_path).lower() not in raw_files_relative:
                    try:
                        print(f"Deleting orphan asset: {rel_path}")
                        dest_path.unlink()
                        deleted_count += 1
                    except Exception as e:
                        print(f"Error deleting orphan asset {rel_path}: {e}")

    # 캐시 파일 쓰기
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_cache, f, indent=2, ensure_ascii=False)
        
    print(f"Asset optimization finished.")
    print(f"Processed: {processed_count}, Skipped: {skipped_count}, Deleted Orphans: {deleted_count}")

if __name__ == "__main__":
    optimize_all_assets()
