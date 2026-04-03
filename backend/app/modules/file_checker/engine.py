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

        suspicious_strings = result.get(
            "suspicious_strings",
            []
        )

        # --- Baseline file observation event ---
        send_event(
            user_id=user_id,
            session_id=session_id,
            entity_id=entity_id,
            entity_type="session",
            module="file_checker",
            signal="file:observed:file_uploaded",
            confidence=1.0,
            severity="low",
            metadata={
                "file_type": file_type,
                "hash": file_hash,
                "file_path": result.get("file_path")
            }
        )

        logger.warning(f"file type: {file_type}")
        logger.warning(f"file hash: {file_hash}")

        if session_id not in _processed_file_hashes:
            _processed_file_hashes[session_id] = set()

        if file_hash in _processed_file_hashes[session_id]:
            logger.warning("Duplicate file detected — skipping")
            return

        _processed_file_hashes[session_id].add(file_hash)

        if len(_processed_file_hashes[session_id]) > 50:
            _processed_file_hashes[session_id].clear()

        # --- File Type Indicators ---

        if file_type == "DOUBLE_EXT":

            send_event(
                user_id=user_id,
                session_id=session_id,
                entity_id=entity_id,
                entity_type="session",
                module="file_checker",
                signal="file:indicator:double_extension",
                confidence=0.85,
                severity="medium",
                metadata={
                    "file_type": file_type,
                    "hash": file_hash,
                    "file_path": result.get("file_path")
                }
            )

        if file_type == "SCRIPT":

            send_event(
                user_id=user_id,
                session_id=session_id,
                entity_id=entity_id,
                entity_type="session",
                module="file_checker",
                signal="file:indicator:risky_script_type",
                confidence=0.6,
                severity="medium",
                metadata={
                    "file_type": file_type,
                    "hash": file_hash,
                    "file_path": result.get("file_path")
                }
            )

        if file_type == "MACRO_DOC":

            send_event(
                user_id=user_id,
                session_id=session_id,
                entity_id=entity_id,
                entity_type="session",
                module="file_checker",
                signal="file:indicator:macro_enabled_document",
                confidence=0.8,
                severity="medium",
                metadata={
                    "file_type": file_type,
                    "hash": file_hash,
                    "file_path": result.get("file_path")
                }
            )

        if file_type == "UNKNOWN":

            send_event(
                user_id=user_id,
                session_id=session_id,
                entity_id=entity_id,
                entity_type="session",
                module="file_checker",
                signal="file:indicator:unknown_file_type",
                confidence=0.5,
                severity="low",
                metadata={
                    "file_type": file_type,
                    "hash": file_hash,
                    "file_path": result.get("file_path")
                }
            )

        # --- Suspicious Size Indicators ---

        if "abnormally_small_executable" in suspicious_strings:

            send_event(
                user_id=user_id,
                session_id=session_id,
                entity_id=entity_id,
                entity_type="session",
                module="file_checker",
                signal="file:indicator:abnormally_small_executable",
                confidence=0.75,
                severity="medium",
                metadata={
                    "file_type": file_type,
                    "hash": file_hash,
                    "file_path": result.get("file_path")
                }
            )

        if "abnormally_large_file" in suspicious_strings:

            send_event(
                user_id=user_id,
                session_id=session_id,
                entity_id=entity_id,
                entity_type="session",
                module="file_checker",
                signal="file:indicator:abnormally_large_file",
                confidence=0.75,
                severity="medium",
                metadata={
                    "file_type": file_type,
                    "hash": file_hash,
                    "file_path": result.get("file_path")
                }
            )

        # --- YARA EVENTS ---

        if file_type in [
            "PE",
            "ELF",
            "SCRIPT",
            "BIN",
            "MACRO_DOC",
            "DOUBLE_EXT"
        ]:

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
                    severity=hit.get(
                        "severity",
                        "medium"
                    ),
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

        count = len(suspicious_strings)

        # --- Archive Signals ---

        if "archive_contains_script" in suspicious_strings:

            send_event(
                user_id=user_id,
                session_id=session_id,
                entity_id=entity_id,
                entity_type="session",
                module="file_checker",
                signal="file:archive:contains_script",
                confidence=0.8,
                severity="medium",
                metadata={
                    "hash": file_hash,
                    "file_path": result.get("file_path")
                }
            )

        if "archive_double_extension" in suspicious_strings:

            send_event(
                user_id=user_id,
                session_id=session_id,
                entity_id=entity_id,
                entity_type="session",
                module="file_checker",
                signal="file:archive:double_extension",
                confidence=0.85,
                severity="medium",
                metadata={
                    "hash": file_hash,
                    "file_path": result.get("file_path")
                }
            )

        # --- Base64 Detection ---

        if "base64_encoded_payload" in suspicious_strings:

            send_event(
                user_id=user_id,
                session_id=session_id,
                entity_id=entity_id,
                entity_type="session",
                module="file_checker",
                signal="file:obfuscation:base64_payload",
                confidence=0.75,
                severity="medium",
                metadata={
                    "hash": file_hash,
                    "file_path": result.get("file_path")
                }
            )

        # --- LOLBIN + Execution Chains ---

        for s in suspicious_strings:

            if s.startswith("lolbin_usage:"):

                send_event(
                    user_id=user_id,
                    session_id=session_id,
                    entity_id=entity_id,
                    entity_type="session",
                    module="file_checker",
                    signal="file:execution:lolbin_usage",
                    confidence=0.8,
                    severity="medium",
                    metadata={
                        "lolbin": s,
                        "hash": file_hash,
                        "file_path": result.get("file_path")
                    }
                )

            if s.startswith("execution_chain:"):

                send_event(
                    user_id=user_id,
                    session_id=session_id,
                    entity_id=entity_id,
                    entity_type="session",
                    module="file_checker",
                    signal="file:execution:suspicious_chain",
                    confidence=0.8,
                    severity="high",
                    metadata={
                        "chain": s,
                        "hash": file_hash,
                        "file_path": result.get("file_path")
                    }
                )

        # --- Suspicious String Escalation ---

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

        # --- Entropy Detection ---

        if entropy > 7.6 and file_type in [
            "PE",
            "ELF",
            "BIN",
            "SCRIPT"
        ]:

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