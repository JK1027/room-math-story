import os
import shutil

src_dir = r"C:\Users\user\.gemini\antigravity-ide\brain\23344a9e-75b3-4410-b396-4a60337447f4"
base_dest_dir = r"c:\Coding\Projects\School\room-math-story\images\중1"

# 매핑 규칙 정의
mappings = {
    "s08": "좌표평면과통계",
    "s12": "평면도형"
}

for prefix, unit_dir in mappings.items():
    dest_dir = os.path.join(base_dest_dir, unit_dir)
    os.makedirs(dest_dir, exist_ok=True)
    
    # 뇌(brain) 폴더에서 해당 접두사로 시작하는 이미지 탐색
    for filename in os.listdir(src_dir):
        if filename.startswith(prefix) and filename.endswith(".png"):
            # 이전 턴에 복사 완료된 파일은 중복 복사 방지 (시간 기반 탐색)
            # 여기서는 새로 생성된 타임스탬프 파일을 찾음
            # s08_ending_1783506389581.png 등
            if "_" in filename:
                parts = filename.split("_")
                # parts[0]: 's08', parts[1]: 'ending', parts[2]: '1783506389581.png'
                if len(parts) >= 3:
                    clean_name = f"{parts[0][1:]}_{parts[1]}.png" # 's08' -> '08_ending.png'
                    src_path = os.path.join(src_dir, filename)
                    dest_path = os.path.join(dest_dir, clean_name)
                    
                    shutil.copy2(src_path, dest_path)
                    print(f"Copied {filename} -> {unit_dir}/{clean_name}")
