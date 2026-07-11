import os
import shutil

src_dir = r"C:\Users\user\.gemini\antigravity-ide\brain\23344a9e-75b3-4410-b396-4a60337447f4"
base_dest_dir = r"c:\Coding\Projects\School\room-math-story\images\중2"

# 중2 에피소드별 매핑 정보
mappings = {
    "s02": "식의계산과연립방정식",
    "s05": "부등식과확률",
    "s06": "도형의성질과닮음",
    "s09": "일차함수"
}

for prefix, unit_dir in mappings.items():
    dest_dir = os.path.join(base_dest_dir, unit_dir)
    os.makedirs(dest_dir, exist_ok=True)
    
    # 뇌(brain) 폴더에서 해당 중2 접두사 파일 찾기
    for filename in os.listdir(src_dir):
        if filename.startswith(prefix) and filename.endswith(".png"):
            if "_" in filename:
                parts = filename.split("_")
                # s02_intro_12345.png -> 02_intro.png
                if len(parts) >= 3:
                    clean_name = f"{parts[0][1:]}_{parts[1]}.png"
                    src_path = os.path.join(src_dir, filename)
                    dest_path = os.path.join(dest_dir, clean_name)
                    
                    shutil.copy2(src_path, dest_path)
                    print(f"Copied {filename} -> {unit_dir}/{clean_name}")
