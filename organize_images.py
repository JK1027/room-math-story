import os
import shutil

images_dir = r"c:\Coding\Projects\School\room-math-story\images"

# 에피소드 11(입체도형)의 이미지들이 속할 학년 및 단원 폴더 지정
target_dir = os.path.join(images_dir, "중1", "입체도형")
os.makedirs(target_dir, exist_ok=True)

# 이동할 이미지 파일 리스트
images_to_move = [
    "01_factory_intro.png",
    "02_cube_bot_blueprint.png",
    "03_stage1_polyhedrons.png",
    "04_stage2_pistons.png",
    "05_stage3_cooling.png",
    "06_factory_ending.png"
]

# 이미지 파일들을 새 하위 폴더로 이동
for img_name in images_to_move:
    src_path = os.path.join(images_dir, img_name)
    dest_path = os.path.join(target_dir, img_name)
    
    if os.path.exists(src_path):
        shutil.move(src_path, dest_path)
        print(f"Moved image: {img_name} -> images/중1/입체도형/")
    else:
        print(f"Image not found at source: {src_path}")
