from app.modules.module_adapter import send_event
from app.modules.file_checker.scanner.scanner import scan_file


def run_file_scan(file_path: str, entity_id: str):
    """
    PHEMA wrapper for malicious file scanner.
    """

    result = scan_file(file_path)

    # 1️⃣ YARA hits → high signal
    for hit in result.get("yara_hits", []):
        send_event(
            entity_id=entity_id,
            entity_type="file",
            module="file_checker",
            signal=hit.get("rule"),
            confidence=0.9,
            severity=hit.get("severity", "medium"),
            metadata={
                "category": hit.get("category"),
                "description": hit.get("description"),
                "hash": result.get("hash"),
                "file_path": result.get("file_path")
            }
        )

    # 2️⃣ Suspicious strings → medium signal
    for pattern in result.get("suspicious_strings", []):
        send_event(
            entity_id=entity_id,
            entity_type="file",
            module="file_checker",
            signal=f"suspicious_string:{pattern}",
            confidence=0.7,
            severity="medium",
            metadata={
                "hash": result.get("hash"),
                "file_path": result.get("file_path")
            }
        )

    # 3️⃣ High entropy → obfuscation signal
    if result.get("entropy", 0) > 7.0:
        send_event(
            entity_id=entity_id,
            entity_type="file",
            module="file_checker",
            signal="high_entropy_file",
            confidence=0.75,
            severity="high",
            metadata={
                "entropy": result.get("entropy"),
                "hash": result.get("hash"),
                "file_path": result.get("file_path")
            }
        )
