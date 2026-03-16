def levenshtein_distance(a: str, b: str) -> int:
    """
    Compute Levenshtein edit distance between two strings.
    """
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    rows = len(a) + 1
    cols = len(b) + 1
    dist = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        dist[i][0] = i
    for j in range(cols):
        dist[0][j] = j

    for i in range(1, rows):
        for j in range(1, cols):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dist[i][j] = min(
                dist[i - 1][j] + 1,      # deletion
                dist[i][j - 1] + 1,      # insertion
                dist[i - 1][j - 1] + cost  # substitution
            )

    return dist[-1][-1]


def tokenize(text: str) -> list:
    """
    Tokenize a string into lowercase alphanumeric tokens.
    """
    if not text:
        return []

    tokens = []
    current = ""

    for ch in text.lower():
        if ch.isalnum():
            current += ch
        else:
            if current:
                tokens.append(current)
                current = ""
    if current:
        tokens.append(current)

    return tokens
