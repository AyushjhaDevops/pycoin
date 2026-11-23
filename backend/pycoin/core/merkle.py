"""Merkle tree utilities for PyCoin."""

from pycoin.crypto.hashing import sha256

LEAF_PREFIX = b"PyCoin:Merkle:Leaf:v1:"
NODE_PREFIX = b"PyCoin:Merkle:Node:v1:"
EMPTY_PREFIX = b"PyCoin:Merkle:Empty:v1"


def _hash_leaf(transaction: bytes) -> bytes:
    """Hash a transaction as a Merkle leaf."""
    if not isinstance(transaction, bytes):
        raise TypeError("transaction must be bytes")

    payload = len(transaction).to_bytes(8, "big") + transaction
    return sha256(LEAF_PREFIX + payload)


def _hash_node(left: bytes, right: bytes) -> bytes:
    """Hash two child nodes into a parent node."""
    return sha256(NODE_PREFIX + left + right)


def merkle_root(transactions: tuple[bytes, ...] | list[bytes]) -> str:
    """Calculate the hexadecimal Merkle root of transaction payloads."""
    if not isinstance(transactions, (tuple, list)):
        raise TypeError("transactions must be a tuple or list")

    if not transactions:
        return sha256(EMPTY_PREFIX).hex()

    level = [_hash_leaf(transaction) for transaction in transactions]

    while len(level) > 1:
        if len(level) % 2 != 0:
            level.append(level[-1])

        next_level = []

        for index in range(0, len(level), 2):
            parent = _hash_node(level[index], level[index + 1])
            next_level.append(parent)

        level = next_level

    return level[0].hex()
