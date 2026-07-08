import os
import shutil

stories_dir = r"c:\Coding\Projects\School\room-math-story\stories"

# 학년별 스토리 매핑 정보
grade_mapping = {
    "중1": [
        "01_time_travel_joseon.txt",
        "04_spy_bomb.txt",
        "08_ghost_ship.txt",
        "11_solid_geometry.txt",
        "12_plane_geometry.txt"
    ],
    "중2": [
        "02_mars_survival.txt",
        "05_zombie_lab.txt",
        "06_deep_sea.txt",
        "09_cyberpunk_metaverse.txt"
    ],
    "중3": [
        "03_magic_academy.txt",
        "07_pyramid_curse.txt",
        "10_detective_holmes.txt"
    ]
}

# 각 학년별 폴더 생성 및 파일 이동
for grade, filenames in grade_mapping.items():
    grade_dir = os.path.join(stories_dir, grade)
    os.makedirs(grade_dir, exist_ok=True)
    
    for filename in filenames:
        src_path = os.path.join(stories_dir, filename)
        dest_path = os.path.join(grade_dir, filename)
        
        if os.path.exists(src_path):
            shutil.move(src_path, dest_path)
            print(f"Moved {filename} -> stories/{grade}/")
        else:
            print(f"File not found: {src_path} (Already moved or doesn't exist)")
