import os
import sys
import glob
import shutil
import argparse
from pathlib import Path

# --- Central Configs Loading ---
_cur = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(os.path.dirname(_cur))
if _root not in sys.path:
    sys.path.append(_root)
from scripts.config import paths

def deploy_grade(grade_key):
    """
    Deploys a specific grade's HTML templates to the corresponding GAS directory.
    grade_key: 'grade1', 'grade2', or 'grade3'
    """
    mapping = {
        "grade1": {"prefix": "m1", "project": "m1_project", "label": "Middle 1"},
        "grade2": {"prefix": "m2", "project": "m2_project", "label": "Middle 2"},
        "grade3": {"prefix": "m3", "project": "m3_project", "label": "Middle 3"}
    }
    
    cfg = mapping.get(grade_key)
    if not cfg:
        print(f"Error: Invalid grade key '{grade_key}'")
        return False
        
    prefix = cfg["prefix"]
    gas_dir = paths.GAS_DIR / cfg["project"]
    os.makedirs(gas_dir, exist_ok=True)
    
    html_pattern = str(paths.APPS_DIR / f"app_{prefix}_*_escape_room.html")
    html_files = glob.glob(html_pattern)
    
    if not html_files:
        print(f"[-] No HTML files found for {cfg['label']} (pattern: {html_pattern})")
        return True
        
    count = 0
    for filepath in html_files:
        filename = os.path.basename(filepath)
        parts = filename.split('_')
        if len(parts) >= 3:
            unit = f"{parts[1]}_{parts[2]}"  # e.g., m1_01
            new_filename = f"Index_{unit}.html"
            new_filepath = os.path.join(gas_dir, new_filename)
            
            shutil.copyfile(filepath, new_filepath)
            print(f"   [COPY] {filename} -> {new_filename}")
            count += 1
            
    # Clean up legacy Index.html for grade1 if it exists
    if grade_key == "grade1":
        old_index = os.path.join(gas_dir, "Index.html")
        if os.path.exists(old_index):
            os.remove(old_index)
            print("   [CLEANUP] Removed legacy Index.html")
            
    print(f"[+] Successfully deployed {count} templates to {gas_dir} ({cfg['label']})\n")
    return True

def main():
    parser = argparse.ArgumentParser(description="Synchronize HTML apps to Google Apps Script projects.")
    parser.add_argument('--target', type=str, choices=['grade1', 'grade2', 'grade3', 'all'],
                        help="Target deployment grade (grade1, grade2, grade3, or all)")
    args = parser.parse_args()
    
    target = args.target
    
    # Fallback to interactive mode if no target argument is provided
    if not target:
        print("=== GAS Deployment Console ===")
        print("Available targets:")
        print(" [1] grade1 (Middle School Year 1)")
        print(" [2] grade2 (Middle School Year 2)")
        print(" [3] grade3 (Middle School Year 3)")
        print(" [4] all (Deploy all grades)")
        print(" [0] exit")
        
        try:
            choice = input("Select target (0-4): ").strip()
        except KeyboardInterrupt:
            print("\nDeployment cancelled.")
            sys.exit(0)
            
        if choice == '1':
            target = 'grade1'
        elif choice == '2':
            target = 'grade2'
        elif choice == '3':
            target = 'grade3'
        elif choice == '4':
            target = 'all'
        elif choice in ('0', ''):
            print("Exiting deployment.")
            sys.exit(0)
        else:
            print("Error: Invalid choice.")
            sys.exit(1)
            
    print(f"\nInitiating deployment to GAS for target: {target}...\n")
    
    if target == 'all':
        for gk in ['grade1', 'grade2', 'grade3']:
            deploy_grade(gk)
    else:
        deploy_grade(target)
        
    print("Deployment cycle completed.")

if __name__ == "__main__":
    main()
