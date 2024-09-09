from __future__ import annotations

import base64
import hashlib


def stable_hash(s: str) -> int:
    """Returns a stable hash of the given string. not cryptographically secure, but stable between runs"""
    # init hash object and update with string
    if isinstance(s, str):
        s = bytes(s, "UTF-8")
    hash_obj: hashlib._Hash = hashlib.sha256(s)
    # get digest and convert to int
    return int.from_bytes(hash_obj.digest(), "big")


def base64_hash(s: str | bytes) -> str:
    """Returns a base64 representation of the hash of the given string. not cryptographically secure"""
    if isinstance(s, str):
        s = bytes(s, "UTF-8")
    hash_bytes: bytes = hashlib.sha256(s).digest()
    hash_b64: str = base64.b64encode(hash_bytes, altchars=b"-_").decode()
    return hash_b64
