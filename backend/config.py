from pathlib import Path
import os

# ONLY CHANGE: __file__ fallback for notebook environments
try:
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
except NameError:
    # Notebook fallback
    cwd = Path(os.getcwd()).resolve()

    # If already in project root
    if (cwd / "backend").exists() and (cwd / "frontend").exists():
        PROJECT_ROOT = cwd
    # If inside /kaggle/working and project folder exists
    elif (cwd / "yoga-rag-microapp").exists():
        PROJECT_ROOT = cwd / "yoga-rag-microapp"
    else:
        # Last fallback: search upwards
        PROJECT_ROOT = None
        for p in [cwd] + list(cwd.parents):
            if (p / "backend").exists() and (p / "frontend").exists():
                PROJECT_ROOT = p
                break
        if PROJECT_ROOT is None:
            raise RuntimeError("Could not locate project root. Please cd into project folder.")

DATA_PATH = PROJECT_ROOT / "data" / "yoga_docs"
VECTOR_DB_PATH = PROJECT_ROOT / "faiss_index"
