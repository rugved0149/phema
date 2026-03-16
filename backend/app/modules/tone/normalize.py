import re


def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower()

    # Normalize time-related patterns
    text = re.sub(r"\b\d+\s*(minutes?|mins?|hours?|hrs?)\b", "<TIME_LIMIT>", text)

    # Remove punctuation (keep words and placeholders)
    text = re.sub(r"[^\w\s<>]", " ", text)

    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text
