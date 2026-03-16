import math
from collections import Counter


def shannon_entropy(text: str) -> float:
    """
    Calculate Shannon entropy of a string.
    Used to detect obfuscated or random-looking URL paths/queries.
    """
    if not text:
        return 0.0

    length = len(text)
    frequencies = Counter(text)

    entropy = 0.0
    for count in frequencies.values():
        p = count / length
        entropy -= p * math.log2(p)

    return entropy
