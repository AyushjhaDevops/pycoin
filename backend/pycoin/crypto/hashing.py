"""SHA-256 hashing utilities for PyCoin."""

import hashlib


def sha256(data: bytes) -> bytes:
    """Return the SHA-256 digest of bytes."""
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")

    return hashlib.sha256(data).digest()


def sha256_hex(data: bytes) -> str:
    """Return the SHA-256 digest as a lowercase hexadecimal string."""
    return sha256(data).hex()
