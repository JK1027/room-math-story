import os
import glob
import re

builder_dir = 'scripts/builders'
py_files = glob.glob(os.path.join(builder_dir, '*.py'))

for fpath in py_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We want to replace html_file = 'app_...' with an absolute path to apps_dir
    # But only if it doesn't already have it
    if 'apps_dir = ' not in content:
        # Match html_file = 'app_...' or html_file = "app_..."
        pattern = r"(html_file\s*=\s*['\"])(app_[^'\"]+\.html)(['\"])"
        
        def repl(m):
            return f'''import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
apps_dir = os.path.join(project_root, "apps")
html_file = os.path.join(apps_dir, "{m.group(2)}")'''

        new_content = re.sub(pattern, repl, content)

        # Also, if there is html_path = os.path.join(base_dir, html_file), we should make sure html_path = html_file, 
        # or just leave it if we redefine base_dir = apps_dir
        # Actually, let's just replace ase_dir = os.path.dirname(os.path.abspath(__file__)) 
        # with ase_dir = apps_dir
        new_content = new_content.replace(
            "base_dir = os.path.dirname(os.path.abspath(__file__))",
            "base_dir = apps_dir"
        )
        
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {fpath}")

