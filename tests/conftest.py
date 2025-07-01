import sys
from pathlib import Path

# Ensure the repository root is on sys.path so that 'app' package can be imported
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
