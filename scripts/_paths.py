"""Path bootstrap for root-level subtitle scripts."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = PROJECT_ROOT / "python"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


def add_main_paths(*, include_scripts: bool = False) -> None:
    python_path = str(PYTHON_DIR)
    if python_path not in sys.path:
        sys.path.insert(0, python_path)
    if include_scripts:
        scripts_path = str(SCRIPTS_DIR)
        if scripts_path not in sys.path:
            sys.path.append(scripts_path)


def project_path(*parts: str) -> Path:
    return PROJECT_ROOT.joinpath(*parts)
