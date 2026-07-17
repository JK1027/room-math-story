import os
import sys
import argparse

# --- Central Configs Loading ---
_cur = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(_cur)
if _root not in sys.path:
    sys.path.append(_root)
from src.runner import run_pipeline

# 23개 단원 리스트 정의
ALL_UNITS = [
    # grade1
    ("grade1", "m1_01"), ("grade1", "m1_02"), ("grade1", "m1_03"), ("grade1", "m1_04"),
    ("grade1", "m1_05"), ("grade1", "m1_06"), ("grade1", "m1_07"), ("grade1", "m1_08"),
    # grade2
    ("grade2", "m2_01"), ("grade2", "m2_02"), ("grade2", "m2_03"), ("grade2", "m2_04"),
    ("grade2", "m2_05"), ("grade2", "m2_06"), ("grade2", "m2_07"), ("grade2", "m2_08"),
    # grade3
    ("grade3", "m3_01"), ("grade3", "m3_02"), ("grade3", "m3_03"), ("grade3", "m3_04"),
    ("grade3", "m3_05"), ("grade3", "m3_06"), ("grade3", "m3_07")
]

def main():
    parser = argparse.ArgumentParser(description="Generic Escape Room Webapp Compiler")
    parser.add_argument('--unit', type=str, default=None, help='Target a single unit (e.g. m1_02)')
    parser.add_argument('--all', action='store_true', help='Compile all 23 math escape room games')
    args = parser.parse_args()
    
    if args.all:
        print("Executing E2E compilation for all 23 games...")
        success_count = 0
        for grade_str, unit in ALL_UNITS:
            ok = run_pipeline(grade_str, unit, build_storybook_flag=False, build_game_flag=True)
            if ok:
                success_count += 1
        print(f"\n[+] Full compilation finished. Compiled {success_count}/{len(ALL_UNITS)} games successfully.")
        sys.exit(0 if success_count == len(ALL_UNITS) else 1)
        
    elif args.unit:
        unit = args.unit
        grade_str = "grade1" if "m1_" in unit else ("grade2" if "m2_" in unit else "grade3")
        success = run_pipeline(grade_str, unit, build_storybook_flag=False, build_game_flag=True)
        sys.exit(0 if success else 1)
        
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
