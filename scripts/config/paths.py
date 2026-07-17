import os
from pathlib import Path

# --- Central Path Registry Constants ---
ROOT_DIR = Path(__file__).resolve().parents[2]

STORIES_DIR = ROOT_DIR / "stories"
STORYBOARDS_DIR = ROOT_DIR / "storyboards"
TEMPLATES_DIR = ROOT_DIR / "templates"
GAS_DIR = ROOT_DIR / "gas"
ARCHIVE_DIR = ROOT_DIR / "archive"
LEGACY_DRAFTS_DIR = ARCHIVE_DIR / "drafts"

import yaml

# --- Path-Generation Helpers ---
def story_dir(grade: str) -> Path:
    """Returns the stories folder for a given grade (e.g. grade1, grade2, grade3)."""
    return STORIES_DIR / grade

def storyboard_dir(grade: str) -> Path:
    """Returns the storyboard folder for a given grade, targeting the generated directory."""
    return STORYBOARDS_DIR / "generated" / grade

def storyboard_path(grade: str, unit: str) -> Path:
    """Returns the full path to a storyboard markdown file."""
    return storyboard_dir(grade) / f"{unit}_storyboard.md"

def story_path(grade: str, unit_code: str) -> Path:
    """Returns the full path to the resolved story markdown file using metadata.yaml maps."""
    meta_path = story_dir(grade) / "metadata.yaml"
    filename = f"chapter{unit_code[3:5]}.md" # default fallback
    
    if meta_path.exists():
        try:
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = yaml.safe_load(f) or {}
                filename = meta.get("units", {}).get(unit_code, {}).get("file", filename)
        except Exception:
            pass
            
    return story_dir(grade) / filename

def html_output_path(unit: str) -> Path:
    """Returns the output HTML file path for a compiled app."""
    return ROOT_DIR / "build" / "webapps" / f"app_{unit}_escape_room.html"

def pdf_output_path(grade: str, unit: str) -> Path:
    """Returns the output PDF file path for a compiled storyboard."""
    return storyboard_dir(grade) / f"{unit}_storyboard.pdf"
