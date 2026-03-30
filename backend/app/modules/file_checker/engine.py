from app.modules.module_adapter import send_event
from app.modules.file_checker.scanner.scanner import scan_file
from app.utils.file_handler import delete_file
from app.core.logger import logger

_processed_file_hashes = {}


def run_file_scan(
    user_id: str,
    session_id: str,
    file_path: str,
    entity_id: str
):

    try:

        result = scan_file(file_path)

        file_hash = result.get("hash")
        entropy = result.get("entropy", 0)
        file_type = result.get("file_type", "UNKNOWN")

        logger.warning(f"file type: {file_type}")
        logger.warning(f"file hash: {file_hash}")

        if session_id not in _processed_file_hashes:
            _processed_file_hashes[session_id] = set()

        if file_hash in _processed_file_hashes[session_id]:
            logger.warning("Duplicate file detected — skipping")
            return

        _processed_file_hashes[session_id].add(file_hash)

        if file_type in ["PE","ELF","SCRIPT","BIN"]:

            for hit in result.get("yara_hits", []):

                logger.warning(
                    f"Yara Rule: {hit.get('rule')}"
                )

                send_event(
                    user_id=user_id,
                    session_id=session_id,
                    entity_id=entity_id,
                    entity_type="session",
                    module="file_checker",
                    signal="file:malware:yara_match",
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

        else:

            logger.warning(
                f"Skipping YARA — file type: {file_type}"
            )

        suspicious_strings = result.get(
            "suspicious_strings", []
        )

        count = len(suspicious_strings)

        if count >= 3:

            send_event(
                user_id=user_id,
                session_id=session_id,
                entity_id=entity_id,
                entity_type="session",
                module="file_checker",
                signal="file:indicator:multiple_suspicious_strings",
                confidence=0.7,
                severity="medium",
                metadata={
                    "count": count,
                    "sample": suspicious_strings[:3],
                    "hash": file_hash,
                    "file_path": result.get("file_path")
                }
            )

        elif count == 2:

            send_event(
                user_id=user_id,
                session_id=session_id,
                entity_id=entity_id,
                entity_type="session",
                module="file_checker",
                signal="file:indicator:suspicious_strings_pair",
                confidence=0.6,
                severity="low",
                metadata={
                    "count": count,
                    "sample": suspicious_strings[:2],
                    "hash": file_hash,
                    "file_path": result.get("file_path")
                }
            )
        if entropy > 7.6 and file_type in ["PE","ELF","BIN"]:

            send_event(
                user_id=user_id,
                session_id=session_id,
                entity_id=entity_id,
                entity_type="session",
                module="file_checker",
                signal="file:obfuscation:high_entropy",
                confidence=0.75,
                severity="medium",
                metadata={
                    "entropy": entropy,
                    "hash": file_hash,
                    "file_path": result.get("file_path")
                }
            )

    finally:

        delete_file(file_path)