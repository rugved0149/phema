"""
File type dispatcher for Cyber Shield.
Used for lightweight file-type identification.
"""

def detect_file_type(path: str) -> str:
    try:
        with open(path, "rb") as f:
            header = f.read(8)

        if header.startswith(b"MZ"):
            return "PE"
        elif header.startswith(b"\x7fELF"):
            return "ELF"
        elif header.startswith(b"#!"):
            return "SCRIPT"
        elif header.startswith(b"%PDF"):
            return "PDF"
        elif header.startswith(b"PK"):
            return "ZIP"
        elif path.lower().endswith(".ps1"):
            return "SCRIPT"
        elif path.lower().endswith(".bin"):
            return "BIN"
        else:
            return "UNKNOWN"
    except Exception:
        return "UNKNOWN"