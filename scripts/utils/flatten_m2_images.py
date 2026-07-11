import os
import shutil

base_dir = r"c:\Coding_Notebook\Projects\school\room-math-story\images\중2"

os.makedirs(base_dir, exist_ok=True)

moved_files = []

for item in os.listdir(base_dir):
    item_path = os.path.join(base_dir, item)
    if os.path.isdir(item_path):
        for filename in os.listdir(item_path):
            if not filename.endswith(".png"):
                continue
            
            src_path = os.path.join(item_path, filename)
            # Just move it directly
            dest_path = os.path.join(base_dir, filename)
            # If filename exists, maybe append a suffix, but they seem unique across folders
            if os.path.exists(dest_path):
                dest_path = os.path.join(base_dir, "old_" + filename)
            
            shutil.move(src_path, dest_path)
            moved_files.append(f"{item}/{filename} -> {os.path.basename(dest_path)}")

        try:
            os.rmdir(item_path)
        except OSError:
            pass

# Also create images/중3
os.makedirs(r"c:\Coding_Notebook\Projects\school\room-math-story\images\중3", exist_ok=True)

for log in moved_files:
    print(log)
