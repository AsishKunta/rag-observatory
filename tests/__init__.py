"""Test package for RAG Observatory.

Puts ``backend/`` on the import path so tests can import the ``app`` package
the same way the running service does.
"""

import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
