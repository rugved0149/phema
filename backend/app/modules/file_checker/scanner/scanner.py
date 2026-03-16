"""
Core scanning engine for PHEMA File Checker.
Primary static analysis only (no execution, no identification).

Extracts raw forensic indicators.
No scoring. No verdicts.
"""

from pathlib import Path
from typing import Dict, Any, List

from app.modules.file_checker.scanner.rules_loader import load_yara_rules
from app.modules.file_checker.scanner.utils import calculate_entropy, calculate_hash
from app.modules.file_checker.scanner.file_dispatcher import detect_file_type


YARA_RULES = load_yara_rules()

# Basic suspicious string indicators (extendable)
SUSPICIOUS_PATTERNS = [
    "Invoke-Expression",
    "CreateRemoteThread",
    "VirtualAllocEx",
    "cmd.exe /c",
    "powershell -EncodedCommand",
    "sekurlsa::logonpasswords",
    "WScript.Shell"
]


def extract_suspicious_strings(file_path: str) -> List[str]:
    found = []
    try:
        with open(file_path, "rb") as f:
            content = f.read().decode(errors="ignore")

        for pattern in SUSPICIOUS_PATTERNS:
            if pattern.lower() in content.lower():
                found.append(pattern)

    except Exception:
        pass

    return found


def scan_file(file_path: str) -> Dict[str, Any]:

    path = Path(file_path)

    if not path.exists() or not path.is_file():
        raise ValueError(f"Invalid file path: {file_path}")

    file_hash = calculate_hash(str(path))
    entropy = calculate_entropy(str(path))
    file_type = detect_file_type(str(path))

    yara_hits = []
    suspicious_strings = extract_suspicious_strings(str(path))

    # YARA static matching
    try:
        matches = YARA_RULES.match(str(path))
        for match in matches:
            yara_hits.append({
                "rule": match.rule,
                "severity": match.meta.get("severity", "low"),
                "category": match.meta.get("category", "unknown"),
                "description": match.meta.get("description", "")
            })
    except Exception as e:
        yara_hits.append({
            "rule": "yara_error",
            "severity": "low",
            "category": "analysis_error",
            "description": str(e)
        })

    return {
        "file_path": str(path),
        "hash": file_hash,
        "file_type": file_type,
        "entropy": entropy,
        "yara_hits": yara_hits,
        "suspicious_strings": suspicious_strings
    }
