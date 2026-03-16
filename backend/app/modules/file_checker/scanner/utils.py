"""
Utility functions for Cyber Shield.
Pure helpers only — no analysis logic.

Author: Rugved Suryawanshi
"""

import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from typing import Dict, Any


# ---------- HASHING ----------
def calculate_hash(file_path: str) -> str:
    """
    Compute SHA-256 hash of a file.

    Args:
        file_path: Path to file

    Returns:
        SHA-256 hex digest

    Raises:
        IOError if file cannot be read
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


# ---------- ENTROPY ----------
def calculate_entropy(file_path: str) -> float:
    """
    Calculate Shannon entropy of file bytes.

    Args:
        file_path: Path to file

    Returns:
        Entropy value (0.0–8.0)
    """
    with open(file_path, "rb") as f:
        data = f.read()

    if not data:
        return 0.0

    freq = Counter(data)
    entropy = -sum(
        (count / len(data)) * math.log2(count / len(data))
        for count in freq.values()
    )

    return round(entropy, 2)


# ---------- JSON OUTPUT ----------
def write_json(data: Dict[str, Any], output_path: str) -> None:
    """
    Write dictionary to a JSON file.

    Args:
        data: Serializable dictionary
        output_path: Destination file path
    """
    ensure_parent_dir(output_path)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def ensure_parent_dir(file_path: str) -> None:
    """
    Ensure parent directory of a file exists.

    Args:
        file_path: Target file path
    """
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
