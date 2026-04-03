from pathlib import Path


SCRIPT_EXTENSIONS = (
    ".ps1",
    ".vbs",
    ".js",
    ".bat",
    ".cmd",
    ".hta",
    ".sh",
    ".py"
)

BINARY_EXTENSIONS = (
    ".bin",
    ".dat"
)


def detect_file_type(path: str) -> str:

    try:

        file_path = Path(path)

        with open(path, "rb") as f:

            header = f.read(8)

        name = file_path.name.lower()

        # --- Double Extension Detection ---

        if name.count(".") >= 2:

            parts = name.split(".")

            last_ext = "." + parts[-1]

            second_ext = "." + parts[-2]

            if second_ext in (
                ".pdf",
                ".doc",
                ".docx",
                ".jpg",
                ".png",
                ".txt"
            ) and last_ext in SCRIPT_EXTENSIONS:

                return "DOUBLE_EXT"

        # --- Header Detection ---

        if header.startswith(b"MZ"):
            return "PE"

        elif header.startswith(b"\x7fELF"):
            return "ELF"

        elif header.startswith(b"%PDF"):
            return "PDF"

        elif header.startswith(b"PK"):
            return "ZIP"

        elif header.startswith(b"#!"):
            return "SCRIPT"
        
        elif name.endswith((
            ".docm",
            ".xlsm",
            ".pptm"
        )):
            return "MACRO_DOC"

        # --- Extension Detection ---

        if name.endswith(SCRIPT_EXTENSIONS):
            return "SCRIPT"

        elif name.endswith(BINARY_EXTENSIONS):
            return "BIN"

        return "UNKNOWN"

    except Exception:

        return "UNKNOWN"