"""Block and block-header models for PyCoin."""

import re
import time
from dataclasses import dataclass

from pycoin.core.merkle import merkle_root
from pycoin.core.serialization import canonical_json_bytes
from pycoin.crypto.hashing import sha256_hex

HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")
BLOCK_HASH_PREFIX = b"PyCoin:Block:v1:"


def _validate_hash(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not HASH_PATTERN.fullmatch(value):
        raise ValueError(f"{field_name} must be a 64-character lowercase hex hash")


@dataclass(frozen=True, slots=True)
class BlockHeader:
    """Immutable metadata used to identify and link a block."""

    version: int
    timestamp: int
    previous_hash: str
    merkle_root: str
    nonce: int = 0

    def __post_init__(self) -> None:
        if isinstance(self.version, bool) or not isinstance(self.version, int):
            raise TypeError("version must be an integer")
        if self.version < 1:
            raise ValueError("version must be positive")

        if isinstance(self.timestamp, bool) or not isinstance(self.timestamp, int):
            raise TypeError("timestamp must be an integer")
        if self.timestamp < 0:
            raise ValueError("timestamp cannot be negative")

        if isinstance(self.nonce, bool) or not isinstance(self.nonce, int):
            raise TypeError("nonce must be an integer")
        if self.nonce < 0:
            raise ValueError("nonce cannot be negative")

        _validate_hash(self.previous_hash, "previous_hash")
        _validate_hash(self.merkle_root, "merkle_root")

    def to_dict(self) -> dict[str, int | str]:
        """Return the canonical header fields."""
        return {
            "version": self.version,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "merkle_root": self.merkle_root,
            "nonce": self.nonce,
        }


@dataclass(frozen=True, slots=True)
class Block:
    """Immutable block containing a header and transaction payloads."""

    header: BlockHeader
    transactions: tuple[bytes, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.header, BlockHeader):
            raise TypeError("header must be a BlockHeader")

        if not isinstance(self.transactions, tuple):
            raise TypeError("transactions must be a tuple")

        if any(not isinstance(tx, bytes) for tx in self.transactions):
            raise TypeError("every transaction must be bytes")

        expected_root = merkle_root(self.transactions)
        if self.header.merkle_root != expected_root:
            raise ValueError("header Merkle root does not match transactions")

    @classmethod
    def create(
        cls,
        transactions: tuple[bytes, ...] | list[bytes],
        previous_hash: str,
        timestamp: int | None = None,
        version: int = 1,
        nonce: int = 0,
    ) -> "Block":
        """Construct a block and calculate its Merkle root."""
        if not isinstance(transactions, (tuple, list)):
            raise TypeError("transactions must be a tuple or list")

        transaction_tuple = tuple(transactions)

        if any(not isinstance(tx, bytes) for tx in transaction_tuple):
            raise TypeError("every transaction must be bytes")

        root = merkle_root(transaction_tuple)

        header = BlockHeader(
            version=version,
            timestamp=(
                time.time_ns() // 1_000_000_000 if timestamp is None else timestamp
            ),
            previous_hash=previous_hash,
            merkle_root=root,
            nonce=nonce,
        )

        return cls(header=header, transactions=transaction_tuple)

    @property
    def hash(self) -> str:
        """Return the deterministic SHA-256 hash of this block header."""
        serialized_header = canonical_json_bytes(self.header.to_dict())
        return sha256_hex(BLOCK_HASH_PREFIX + serialized_header)
