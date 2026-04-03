from pathlib import Path
from typing import Dict, Any, List
import re
import zipfile

from app.modules.file_checker.scanner.rules_loader import load_yara_rules
from app.modules.file_checker.scanner.utils import (
    calculate_entropy,
    calculate_hash
)
from app.modules.file_checker.scanner.file_dispatcher import detect_file_type
from app.modules.file_checker.scanner.hash_db import check_hash


YARA_RULES = load_yara_rules()

MAX_FILE_SIZE = 10 * 1024 * 1024

BASE64_PATTERN = re.compile(
    rb"[A-Za-z0-9+/]{200,}={0,2}"
)

SUSPICIOUS_PATTERNS = [

"CreateRemoteThread",
"VirtualAllocEx",
"WriteProcessMemory",
"NtQueryInformationProcess",
"sekurlsa::logonpasswords",
"powershell -EncodedCommand",
"Invoke-Expression"

]

LOLBIN_PATTERNS = [

"powershell",
"mshta",
"certutil",
"bitsadmin",
"rundll32",
"wscript",
"cscript"

]

EXECUTION_CHAIN_PATTERNS = [

("cmd.exe","powershell"),
("powershell","certutil"),
("powershell","bitsadmin"),
("mshta","powershell"),
"cmd.exe /c powershell",
"powershell -enc",
"powershell -encodedcommand",
"certutil -urlcache",
"bitsadmin /transfer"

]


def detect_base64(file_path: str) -> int:

    try:

        with open(file_path, "rb") as f:

            data = f.read()

        matches = BASE64_PATTERN.findall(data)

        return len(matches)

    except:

        return 0


def inspect_zip_contents(file_path: str) -> List[str]:

    suspicious = []

    try:

        with zipfile.ZipFile(file_path, "r") as z:

            names = z.namelist()

            for name in names:

                lowered = name.lower()

                if lowered.endswith((
                    ".js",
                    ".vbs",
                    ".ps1",
                    ".bat",
                    ".cmd",
                    ".hta"
                )):

                    suspicious.append(
                        "archive_contains_script"
                    )

                if lowered.count(".") >= 2:

                    suspicious.append(
                        "archive_double_extension"
                    )

    except Exception:

        pass

    return suspicious


def extract_suspicious_strings(file_path: str) -> List[str]:

    found = set()

    try:

        with open(file_path, "rb") as f:

            while True:

                chunk = f.read(8192)

                if not chunk:
                    break

                text = chunk.decode(
                    errors="ignore"
                ).lower()

                for pattern in SUSPICIOUS_PATTERNS:

                    p = pattern.lower()

                    if len(p) >= 10 and p in text:

                        found.add(pattern)

                for lolbin in LOLBIN_PATTERNS:

                    if lolbin in text:

                        found.add(
                            f"lolbin_usage:{lolbin}"
                        )

    except Exception:

        pass

    return list(found)

def detect_size_anomaly(path, file_type):

    size = path.stat().st_size

    suspicious = []

    if file_type in ["PE","SCRIPT","BIN"]:

        if size < 2048:

            suspicious.append(
                "abnormally_small_executable"
            )

        if size > 20_000_000:

            suspicious.append(
                "abnormally_large_file"
            )

    return suspicious

def detect_execution_chain(file_path):

    try:

        with open(file_path,"rb") as f:

            text = f.read().decode(
                errors="ignore"
            ).lower()

        detected = []

        for a,b in EXECUTION_CHAIN_PATTERNS:

            if a in text and b in text:

                detected.append(
                    f"execution_chain:{a}->{b}"
                )

        return detected

    except:

        return []

def scan_file(file_path: str) -> Dict[str, Any]:

    path = Path(file_path)

    if not path.exists() or not path.is_file():

        raise ValueError(
            f"Invalid file path: {file_path}"
        )

    if path.stat().st_size > MAX_FILE_SIZE:

        return {
            "file_path": str(path),
            "hash": calculate_hash(str(path)),
            "file_type": "LARGE_FILE",
            "entropy": 0,
            "yara_hits": [],
            "suspicious_strings": []
        }

    file_hash = calculate_hash(str(path))
    entropy = calculate_entropy(str(path))
    file_type = detect_file_type(str(path))
    suspicious_strings = []

    size_flags = detect_size_anomaly(
        path,
        file_type
    )

    suspicious_strings.extend(
        size_flags
    )

    chain_flags = detect_execution_chain(
        str(path)
    )

    suspicious_strings.extend(
        chain_flags
    )

    if file_type == "PDF":

        return {
            "file_path": str(path),
            "hash": file_hash,
            "file_type": file_type,
            "entropy": entropy,
            "yara_hits": [],
            "suspicious_strings": []
        }

    yara_hits = []

    suspicious_strings = extract_suspicious_strings(
        str(path)
    )

    base64_hits = detect_base64(
        str(path)
    )

    if base64_hits > 0:

        suspicious_strings.append(
            "base64_encoded_payload"
        )

    if file_type == "ZIP":

        zip_flags = inspect_zip_contents(
            str(path)
        )

        suspicious_strings.extend(
            zip_flags
        )

    known_hash_name = check_hash(
        file_hash
    )

    if known_hash_name:

        yara_hits.append({

            "rule": "known_hash_match",
            "severity": "high",
            "category": "malware_hash",
            "description": known_hash_name

        })

    if file_type in [

        "PE",
        "ELF",
        "SCRIPT",
        "BIN",
        "MACRO_DOC"

    ]:

        try:

            matches = YARA_RULES.match(
                str(path)
            )

            seen_rules = set()

            for match in matches:

                rule_name = match.rule

                if rule_name in seen_rules:
                    continue

                seen_rules.add(rule_name)

                yara_hits.append({

                    "rule": rule_name,
                    "severity": match.meta.get(
                        "severity",
                        "low"
                    ),
                    "category": match.meta.get(
                        "category",
                        "unknown"
                    ),
                    "description": match.meta.get(
                        "description",
                        ""
                    )

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