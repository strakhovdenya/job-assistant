import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_PATH = PROJECT_ROOT / "apps" / "frontend"

sys.path.insert(0, str(FRONTEND_PATH))