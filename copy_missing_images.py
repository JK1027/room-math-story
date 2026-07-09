import os
import shutil
import glob

artifact_dir = r"C:\Users\USER\.gemini\antigravity-ide\brain\44125b77-29ef-4bae-8599-ad4801eaae6c"
base_dest_dir = r"c:\Coding_Notebook\Projects\school\room-math-story\images\중1"

mappings = {
    "02_": ("수와연산", "02_"),
    "coord_": ("좌표평면과통계", "04_"),
    "geom_": ("기본도형", "05_")
}

for filename in os.listdir(artifact_dir):
    if not filename.endswith(".png"):
        continue

    for prefix, (unit_dir, new_prefix) in mappings.items():
        if filename.startswith(prefix):
            dest_dir = os.path.join(base_dest_dir, unit_dir)
            os.makedirs(dest_dir, exist_ok=True)

            # extract base name (remove timestamp: prefix_name_1234.png -> new_prefix_name.png)
            # Example: coord_whirlpool_1783557029308.png -> coord_whirlpool
            parts = filename.split("_")
            if len(parts) >= 3:
                # The last part is timestamp.png, so we join everything before that.
                # e.g. coord_whirlpool_1234.png -> coord, whirlpool, 1234.png
                # If prefix is coord_, base_name is 'whirlpool'
                base_name = "_".join(parts[1:-1])
                clean_name = f"{new_prefix}{base_name}.png"

                src_path = os.path.join(artifact_dir, filename)
                dest_path = os.path.join(dest_dir, clean_name)

                shutil.copy2(src_path, dest_path)
                print(f"Copied {filename} -> {unit_dir}/{clean_name}")
