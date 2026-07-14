import os
import glob
import shutil

apps_dir = r"c:\Coding\Projects\School\room-math-story\apps"
gas_dir = r"c:\Coding\Projects\School\room-math-story\GAS\m1_project"

# Ensure the m1_project directory exists
os.makedirs(gas_dir, exist_ok=True)

# Find all middle school year 1 HTML apps
html_files = glob.glob(os.path.join(apps_dir, "app_m1_*_escape_room.html"))

count = 0
for filepath in html_files:
    filename = os.path.basename(filepath)
    # Extract unit part, e.g., 'm1_01' from 'app_m1_01_escape_room.html'
    parts = filename.split('_')
    if len(parts) >= 3:
        unit = f"{parts[1]}_{parts[2]}"  # m1_01
        
        # New filename: Index_m1_01.html
        new_filename = f"Index_{unit}.html"
        new_filepath = os.path.join(gas_dir, new_filename)
        
        # Copy file
        shutil.copyfile(filepath, new_filepath)
        print(f"Copied: {filename} -> {new_filename}")
        count += 1

# Also check for Index.html (the old one) and remove it if it exists to prevent confusion
old_index = os.path.join(gas_dir, "Index.html")
if os.path.exists(old_index):
    os.remove(old_index)
    print(f"Removed legacy Index.html")

print(f"Successfully synchronized {count} HTML templates to {gas_dir}")
