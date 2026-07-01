"""Path bootstrap for the vr_subtitle subproject."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN_ROOT = PROJECT_ROOT.parent
MAIN_PYTHON = MAIN_ROOT / "python"
MAIN_SCRIPTS = MAIN_ROOT / "scripts"


def add_main_paths(*, include_scripts: bool = False) -> None:
    python_path = str(MAIN_PYTHON)
    if python_path not in sys.path:
        sys.path.insert(0, python_path)
    if include_scripts:
        scripts_path = str(MAIN_SCRIPTS)
        if scripts_path not in sys.path:
            sys.path.append(scripts_path)


def project_path(*parts: str) -> Path:
    return PROJECT_ROOT.joinpath(*parts)
