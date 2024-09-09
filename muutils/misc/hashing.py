from __future__ import annotations

import base64
import hashlib


def stable_hash(s: str | bytes) -> int:
    """Returns a stable hash of the given string. not cryptographically secure, but stable between runs"""
    # init hash object and update with string
    s_bytes: bytes
    if isinstance(s, str):
        s_bytes = bytes(s, "UTF-8")
    else:
        s_bytes = s
    hash_obj: hashlib._Hash = hashlib.sha256(s_bytes)
    # get digest and convert to int
    return int.from_bytes(hash_obj.digest(), "big")


def base64_hash(s: str | bytes) -> str:
    """Returns a base64 representation of the hash of the given string. not cryptographically secure"""
    s_bytes: bytes
    if isinstance(s, str):
        s_bytes = bytes(s, "UTF-8")
    else:
        s_bytes = s
    hash_bytes: bytes = hashlib.sha256(s_bytes).digest()
    hash_b64: str = base64.b64encode(hash_bytes, altchars=b"-_").decode()
    return hash_b64
