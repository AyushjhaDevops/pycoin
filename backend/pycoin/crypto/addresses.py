"""Versioned PyCoin address derivation and validation."""

import base64
import binascii

from pycoin.crypto.hashing import sha256

ADDRESS_PREFIX = "PYC1"

_ADDRESS_DOMAIN = b"PyCoin:Address:v1:"
_CHECKSUM_DOMAIN = b"PyCoin:AddressChecksum:v1:"

VERSION = 1
PAYLOAD_SIZE = 20
CHECKSUM_SIZE = 4
PUBLIC_KEY_SIZE = 32


def derive_address(public_key: bytes) -> str:
    """Derive a deterministic PYC address from an Ed25519 public key."""
    if not isinstance(public_key, bytes):
        raise TypeError("public_key must be bytes")

    if len(public_key) != PUBLIC_KEY_SIZE:
        raise ValueError("Ed25519 public key must be 32 bytes")

    payload = sha256(_ADDRESS_DOMAIN + public_key)[:PAYLOAD_SIZE]
    versioned_payload = bytes([VERSION]) + payload

    checksum = sha256(_CHECKSUM_DOMAIN + versioned_payload)[:CHECKSUM_SIZE]

    encoded = base64.b32encode(versioned_payload + checksum).decode("ascii").rstrip("=")

    return ADDRESS_PREFIX + encoded


def is_valid_address(address: str) -> bool:
    """Validate address prefix, encoding, version, and checksum."""
    if not isinstance(address, str):
        return False

    if not address.startswith(ADDRESS_PREFIX):
        return False

    encoded = address[len(ADDRESS_PREFIX) :]

    # The encoded 25-byte payload must be exactly 40 Base32 characters.
    if len(encoded) != 40:
        return False

    # This format uses uppercase Base32 without padding.
    if not all(char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567" for char in encoded):
        return False

    try:
        decoded = base64.b32decode(encoded, casefold=False)
    except (binascii.Error, ValueError):
        return False

    if len(decoded) != 1 + PAYLOAD_SIZE + CHECKSUM_SIZE:
        return False

    versioned_payload = decoded[:-CHECKSUM_SIZE]
    supplied_checksum = decoded[-CHECKSUM_SIZE:]

    if versioned_payload[0] != VERSION:
        return False

    expected_checksum = sha256(_CHECKSUM_DOMAIN + versioned_payload)[:CHECKSUM_SIZE]

    return supplied_checksum == expected_checksum
