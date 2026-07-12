import os
import glob
import shutil

apps_dir = r"c:\Coding\Projects\School\room-math-story\apps"
gas_dir = r"c:\Coding\Projects\School\room-math-story\GAS\m2_project"

# Ensure the m2_project directory exists
os.makedirs(gas_dir, exist_ok=True)

# Find all middle school year 2 HTML apps
html_files = glob.glob(os.path.join(apps_dir, "app_m2_*_escape_room.html"))

count = 0
for filepath in html_files:
    filename = os.path.basename(filepath)
    # Extract unit part, e.g., 'm2_01' from 'app_m2_01_escape_room.html'
    parts = filename.split('_')
    if len(parts) >= 3:
        unit = f"{parts[1]}_{parts[2]}"  # m2_01
        
        # New filename: Index_m2_01.html
        new_filename = f"Index_{unit}.html"
        new_filepath = os.path.join(gas_dir, new_filename)
        
        # Copy file
        shutil.copyfile(filepath, new_filepath)
        print(f"Copied: {filename} -> {new_filename}")
        count += 1

print(f"Successfully synchronized {count} Middle 2 HTML templates to {gas_dir}")
