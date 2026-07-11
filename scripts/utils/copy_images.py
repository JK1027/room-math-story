import os
import shutil

src_dir = r"C:\Users\user\.gemini\antigravity-ide\brain\23344a9e-75b3-4410-b396-4a60337447f4"
dest_dir = r"c:\Coding\Projects\School\room-math-story\images"
os.makedirs(dest_dir, exist_ok=True)

mapping = {
    "geo_factory_intro_1783429673805.png": "01_factory_intro.png",
    "cube_bot_blueprint_1783429683057.png": "02_cube_bot_blueprint.png",
    "stage1_polyhedrons_1783429697106.png": "03_stage1_polyhedrons.png",
    "stage2_pistons_1783429709271.png": "04_stage2_pistons.png",
    "stage3_cooling_1783429721899.png": "05_stage3_cooling.png",
    "geo_factory_ending_1783429732616.png": "06_factory_ending.png"
}

for src_name, dest_name in mapping.items():
    src_path = os.path.join(src_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dest_path)
        print(f"Copied {src_name} to {dest_name}")
    else:
        print(f"File not found: {src_path}")
