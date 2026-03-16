"""
Simple local malicious hash database.
Used only to emit known-hash detection signals.
"""

# Example static malicious hash list (extendable)
KNOWN_MALICIOUS_HASHES = {
    "e3b0c44298fc1c149afbf4c8996fb924...": "Test_Malware_Sample"
}


def check_hash(hash_value: str):
    if hash_value in KNOWN_MALICIOUS_HASHES:
        return KNOWN_MALICIOUS_HASHES[hash_value]
    return None
