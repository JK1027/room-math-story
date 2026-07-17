import os
import re

project_root = r"c:\Coding\Projects\School\room-math-story"
builders_dir = os.path.join(project_root, "scripts", "builders")

def get_unit_from_filename(filename):
    m2_match = re.search(r'update_app_m2_(\d+)\.py', filename)
    if m2_match:
        return f"m2_{m2_match.group(1).zfill(2)}"
    m3_match = re.search(r'update_app_m3_(\d+)\.py', filename)
    if m3_match:
        return f"m3_{m3_match.group(1).zfill(2)}"
    m1_match = re.search(r'update_app_(\d+)\.py', filename)
    if m1_match:
        return f"m1_{m1_match.group(1).zfill(2)}"
    return None

def main():
    files = sorted(os.listdir(builders_dir))
    
    for filename in files:
        if not filename.startswith("update_app_") or not filename.endswith(".py"):
            continue
            
        unit = get_unit_from_filename(filename)
        if not unit:
            continue
            
        file_path = os.path.join(builders_dir, filename)
        print(f"Patching {filename} ({unit})...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().replace('\r\n', '\n')
            
        # qs\s*=\s*\[ 매칭 및 범위 찾기
        qs_match = re.search(r'qs\s*=\s*\[', content)
        if not qs_match:
            print(f"  Warning: 'qs' list declaration not found in {filename}")
            continue
            
        qs_start = qs_match.start()
        bracket_count = 0
        qs_end = -1
        
        start_bracket_idx = content.find('[', qs_start)
        if start_bracket_idx == -1:
            print(f"  Warning: Bracket matching failed for {filename}")
            continue
            
        for i in range(start_bracket_idx, len(content)):
            char = content[i]
            if char == '[':
                bracket_count += 1
            elif char == ']':
                bracket_count -= 1
                if bracket_count == 0:
                    qs_end = i + 1
                    break
                    
        if qs_end == -1:
            print(f"  Warning: Closing bracket matching failed for {filename}")
            continue
            
        # 대체 코드
        replacement_code = f"""# --- Dynamic Storyboard Loading ---
import sys
import os
_cur = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(os.path.dirname(_cur))
if _root not in sys.path:
    sys.path.append(_root)
from scripts.utils.storyboard_parser import load_storyboard_qs
qs = load_storyboard_qs('{unit}')
# ----------------------------------"""
        
        # 교체 실행
        new_content = content[:qs_start] + replacement_code + content[qs_end:]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  Successfully patched {filename}!")

if __name__ == "__main__":
    main()
