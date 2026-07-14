import os
import glob
import shutil

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
gas_dir = os.path.join(project_root, "GAS", "m3_project")

# Ensure the m3_project directory exists
os.makedirs(gas_dir, exist_ok=True)

# Find all middle school year 3 HTML apps
html_files = glob.glob(os.path.join(apps_dir, "app_m3_*_escape_room.html"))

count = 0
for filepath in html_files:
    filename = os.path.basename(filepath)
    # Extract unit part, e.g., 'm3_01' from 'app_m3_01_escape_room.html'
    parts = filename.split('_')
    if len(parts) >= 3:
        unit = f"{parts[1]}_{parts[2]}"  # m3_01
        
        # New filename: Index_m3_01.html
        new_filename = f"Index_{unit}.html"
        new_filepath = os.path.join(gas_dir, new_filename)
        
        # Copy file
        shutil.copyfile(filepath, new_filepath)
        print(f"Copied: {filename} -> {new_filename}")
        count += 1

print(f"Successfully synchronized {count} Middle 3 HTML templates to {gas_dir}")
