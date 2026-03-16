"""
File type dispatcher for Cyber Shield.
Used for lightweight file-type identification.
"""

def detect_file_type(path: str) -> str:
    try:
        with open(path, "rb") as f:
            header = f.read(4)

        if header.startswith(b"MZ"):
            return "PE"
        elif header.startswith(b"\x7fELF"):
            return "ELF"
        elif header.startswith(b"#!"):
            return "SCRIPT"
        else:
            return "UNKNOWN"
    except Exception:
        return "UNKNOWN"
