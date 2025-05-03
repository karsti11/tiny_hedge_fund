from pathlib import Path

def get_project_root():
    current_dir = Path(__file__).resolve().parent
    return current_dir.parent