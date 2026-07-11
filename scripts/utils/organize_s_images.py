import os
import shutil

src_dir = r"C:\Users\user\.gemini\antigravity-ide\brain\23344a9e-75b3-4410-b396-4a60337447f4"
base_dest_dir = r"c:\Coding\Projects\School\room-math-story\images\중1"

mappings = {
    "s01": "수와연산",
    "s04": "문자와식",
    "s08": "좌표평면과통계"
}

for prefix, unit_dir in mappings.items():
    dest_dir = os.path.join(base_dest_dir, unit_dir)
    os.makedirs(dest_dir, exist_ok=True)
    
    # Find files starting with prefix
    for filename in os.listdir(src_dir):
        if filename.startswith(prefix) and filename.endswith(".png"):
            src_path = os.path.join(src_dir, filename)
            # 깔끔한 파일명으로 변환 (예: s01_intro_12345.png -> 01_intro.png)
            parts = filename.split("_")
            clean_name = f"{parts[0][1:]}_{parts[1]}.png" # s01_intro -> 01_intro.png
            dest_path = os.path.join(dest_dir, clean_name)
            
            shutil.copy2(src_path, dest_path)
            print(f"Copied {filename} -> {unit_dir}/{clean_name}")
