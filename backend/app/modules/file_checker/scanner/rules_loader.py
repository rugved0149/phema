"""
YARA rules loader and compiler.
Primary static analysis only.

Author: Rugved Suryawanshi
"""

import os
from pathlib import Path

try:
    import yara
    YARA_AVAILABLE = True
except ImportError:
    YARA_AVAILABLE = False


# ---------- PATH SETUP (ROBUST) ----------
BASE_DIR = Path(__file__).resolve().parent.parent
RULES_DIR = BASE_DIR / "rules" / "yara"


# ---------- CORE LOADER ----------
def load_yara_rules():
    """
    Load and compile all YARA rules from rules/yara directory.

    Returns:
        yara.Rules object

    Raises:
        RuntimeError if YARA not available or rules missing
    """
    if not YARA_AVAILABLE:
        raise RuntimeError("yara-python is not installed")

    if not RULES_DIR.exists():
        raise RuntimeError(f"Rules directory not found: {RULES_DIR}")

    rule_files = {
        file.name: str(file)
        for file in RULES_DIR.iterdir()
        if file.suffix in (".yar", ".yara")
    }

    if not rule_files:
        raise RuntimeError(f"No YARA rules found in {RULES_DIR}")

    return yara.compile(filepaths=rule_files)


# ---------- ENV CHECK ----------
def check_yara_installation() -> bool:
    return YARA_AVAILABLE


# ---------- INSTALL HELP ----------
def get_installation_help() -> str:
    return """
YARA Installation Help (Windows):

1. Standard pip install:
   pip install yara-python

2. If build fails, use precompiled wheel:
   https://github.com/VirusTotal/yara-python/releases

3. Conda alternative:
   conda install -c conda-forge yara-python

4. Verify installation:
   python -c "import yara; print(yara.__version__)"
"""
