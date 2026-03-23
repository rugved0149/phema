from app.modules.module_adapter import send_event
from app.modules.file_checker.scanner.scanner import scan_file


def run_file_scan(file_path: str, entity_id: str):
    """
    PHEMA wrapper for malicious file scanner.
    """

    result = scan_file(file_path)

    file_hash = result.get("hash")
    entropy = result.get("entropy", 0)

    # -------------------------
    # 1️⃣ YARA hits → high signal (standardized)
    # -------------------------
    for hit in result.get("yara_hits", []):
        send_event(
            entity_id=entity_id,
            entity_type="session",
            module="file_checker",
            signal="file:malware:yara_match",   # ✅ standardized
            confidence=0.9,
            severity=hit.get("severity", "medium"),
            metadata={
                "rule": hit.get("rule"),
                "category": hit.get("category"),
                "description": hit.get("description"),
                "hash": file_hash,
                "file_path": result.get("file_path")
            }
        )

    # -------------------------
    # 2️⃣ Suspicious strings → controlled signal (no flooding)
    # -------------------------
    suspicious_strings = result.get("suspicious_strings", [])

    if suspicious_strings:
        send_event(
            entity_id=entity_id,
            entity_type="session",
            module="file_checker",
            signal="file:indicator:multiple_suspicious_strings",  # ✅ standardized
            confidence=0.7,
            severity="medium",
            metadata={
                "count": len(suspicious_strings),
                "sample": suspicious_strings[:3],  # small preview only
                "hash": file_hash,
                "file_path": result.get("file_path")
            }
        )

    # -------------------------
    # 3️⃣ High entropy → obfuscation signal
    # -------------------------
    if entropy > 7.0:
        send_event(
            entity_id=entity_id,
            entity_type="session",
            module="file_checker",
            signal="file:obfuscation:high_entropy",  # ✅ standardized
            confidence=0.75,
            severity="high",
            metadata={
                "entropy": entropy,
                "hash": file_hash,
                "file_path": result.get("file_path")
            }
        )