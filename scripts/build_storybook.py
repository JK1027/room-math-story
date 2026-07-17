import os
import sys
import argparse

# --- Central Configs Loading ---
_cur = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(_cur)
if _root not in sys.path:
    sys.path.append(_root)
from src.runner import run_pipeline
from scripts.config.constants import SUPPORTED_GRADES

def main():
    parser = argparse.ArgumentParser(description="Storybook Viewer HTML Compiler")
    parser.add_argument('--unit', type=str, default='m1_02', help='Unit ID (e.g. m1_02, m2_01)')
    args = parser.parse_args()
    
    unit = args.unit
    grade_str = "grade1" if "m1_" in unit else ("grade2" if "m2_" in unit else "grade3")
    
    success = run_pipeline(grade_str, unit, build_storybook_flag=True, build_game_flag=False)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
