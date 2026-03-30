"""
Core scanning engine for PHEMA File Checker.
Primary static analysis only (no execution, no identification).

Extracts raw forensic indicators.
No scoring. No verdicts.
"""

from pathlib import Path
from typing import Dict, Any, List

from app.modules.file_checker.scanner.rules_loader import load_yara_rules
from app.modules.file_checker.scanner.utils import (
    calculate_entropy,
    calculate_hash
)
from app.modules.file_checker.scanner.file_dispatcher import detect_file_type
from app.modules.file_checker.scanner.hash_db import check_hash


YARA_RULES = load_yara_rules()


SUSPICIOUS_PATTERNS = [

"CreateRemoteThread",
"VirtualAllocEx",
"WriteProcessMemory",
"NtQueryInformationProcess",
"sekurlsa::logonpasswords",
"powershell -EncodedCommand",
"Invoke-Expression"

]


def extract_suspicious_strings(file_path: str) -> List[str]:

    found = set()

    try:

        with open(file_path, "rb") as f:

            while True:

                chunk = f.read(8192)

                if not chunk:
                    break

                text = chunk.decode(errors="ignore").lower()

                for pattern in SUSPICIOUS_PATTERNS:

                    p = pattern.lower()

                    if len(p) >= 10 and p in text:
                        found.add(pattern)

    except Exception:
        pass

    return list(found)


def scan_file(file_path: str) -> Dict[str, Any]:

    path = Path(file_path)

    if not path.exists() or not path.is_file():
        raise ValueError(f"Invalid file path: {file_path}")

    file_hash = calculate_hash(str(path))
    entropy = calculate_entropy(str(path))
    file_type = detect_file_type(str(path))

    yara_hits = []
    suspicious_strings = extract_suspicious_strings(str(path))

    # --- Known Hash Check ---

    known_hash_name = check_hash(file_hash)

    if known_hash_name:

        yara_hits.append({

            "rule": "known_hash_match",
            "severity": "high",
            "category": "malware_hash",
            "description": known_hash_name

        })

    # --- YARA Matching (Only for executable/script/binary types) ---

    if file_type in ["PE","ELF","SCRIPT","BIN"]:

        try:

            matches = YARA_RULES.match(str(path))

            seen_rules = set()

            for match in matches:

                rule_name = match.rule

                if rule_name in seen_rules:
                    continue

                seen_rules.add(rule_name)

                yara_hits.append({

                    "rule": rule_name,
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