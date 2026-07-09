import os
import shutil

base_dir = r"c:\Coding_Notebook\Projects\school\room-math-story\images\중1"

# Mapping rules: folder_name -> list of (old_prefix, new_prefix)
# Some folders have no prefixes in the file names to replace, so we just add the prefix if it's not there.
# For "입체도형", the filenames start with 01_, 02_, etc. We want to replace "0X_" with "m1_07_".
# Wait, for "입체도형", replacing "01_" with "m1_07_" makes "m1_07_factory_intro.png", which is good, but wait:
# `01_factory_intro.png` -> `m1_07_factory_intro.png`.
# It's better to just write explicit rules or use logic.

tasks = [
    ("수와연산", "01_", "m1_01_"),
    ("수와연산", "02_", "m1_02_"),
    ("문자와식", "04_", "m1_03_"),
    ("좌표평면과통계", "04_", "m1_04_"),
    ("기본도형", "05_", "m1_05_"),
    ("평면도형", "12_", "m1_06_"),
    ("입체도형", "01_", "m1_07_"),
    ("입체도형", "02_", "m1_07_"),
    ("입체도형", "03_", "m1_07_"),
    ("입체도형", "04_", "m1_07_"),
    ("입체도형", "05_", "m1_07_"),
    ("입체도형", "06_", "m1_07_"),
    ("좌표평면과통계", "08_", "m1_08_"),
]

# Specifically for 입체도형, we don't want to replace "01_" with "m1_07_" and lose the "01", 
# wait, actually "factory_intro.png" is fine. The sequence doesn't matter as long as the names are unique.
# Let's map filenames exactly for 입체도형 to be safe, or just prepend `m1_07_` and remove `0X_`.
# "01_factory_intro.png" -> "m1_07_factory_intro.png" (cleaner).

moved_files = []

# Ensure flat directory exists
os.makedirs(base_dir, exist_ok=True)

# List all folders in base_dir
for item in os.listdir(base_dir):
    item_path = os.path.join(base_dir, item)
    if os.path.isdir(item_path):
        for filename in os.listdir(item_path):
            if not filename.endswith(".png"):
                continue
            
            src_path = os.path.join(item_path, filename)
            new_filename = filename
            
            # Apply matching task
            for folder, old_prefix, new_prefix in tasks:
                # We do startswith but we have to be careful with Korean encoding issues in script string vs filesystem.
                # Since we iterate actual folders, we can just check if item matches the folder name's unicode.
                # Actually, in python 3 on windows, os.listdir returns correct unicode.
                if item == folder and filename.startswith(old_prefix):
                    # Replace prefix
                    new_filename = new_prefix + filename[len(old_prefix):]
                    break
            
            dest_path = os.path.join(base_dir, new_filename)
            shutil.move(src_path, dest_path)
            moved_files.append(f"{item}/{filename} -> {new_filename}")

        # Try to remove the directory if it's empty
        try:
            os.rmdir(item_path)
        except OSError:
            pass

for log in moved_files:
    print(log)
