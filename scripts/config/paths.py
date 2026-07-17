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

def story_path(grade: str, script_name: str) -> Path:
    """Returns the full path to a story script markdown file."""
    return story_dir(grade) / script_name

def html_output_path(unit: str) -> Path:
    """Returns the output HTML file path for a compiled app."""
    return ROOT_DIR / "build" / "webapps" / f"app_{unit}_escape_room.html"

def pdf_output_path(grade: str, unit: str) -> Path:
    """Returns the output PDF file path for a compiled storyboard."""
    return storyboard_dir(grade) / f"{unit}_storyboard.pdf"
