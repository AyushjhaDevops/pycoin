"""Tests for PyCoin block structures."""

from dataclasses import FrozenInstanceError

import pytest
from pycoin.core.blocks import Block, BlockHeader
from pycoin.core.merkle import merkle_root

ZERO_HASH = "0" * 64


def test_block_creation_calculates_merkle_root() -> None:
    block = Block.create(
        transactions=(b"tx-1", b"tx-2"),
        previous_hash=ZERO_HASH,
        timestamp=100,
    )

    assert block.header.merkle_root == merkle_root((b"tx-1", b"tx-2"))


def test_block_hash_is_deterministic() -> None:
    first = Block.create((b"tx-1",), ZERO_HASH, timestamp=100)
    second = Block.create((b"tx-1",), ZERO_HASH, timestamp=100)

    assert first.hash == second.hash


def test_transaction_change_changes_block_hash() -> None:
    first = Block.create((b"tx-1",), ZERO_HASH, timestamp=100)
    second = Block.create((b"tx-2",), ZERO_HASH, timestamp=100)

    assert first.hash != second.hash


def test_block_rejects_incorrect_merkle_root() -> None:
    header = BlockHeader(
        version=1,
        timestamp=100,
        previous_hash=ZERO_HASH,
        merkle_root=ZERO_HASH,
    )

    with pytest.raises(ValueError, match="Merkle root"):
        Block(header=header, transactions=(b"tx-1",))


def test_block_rejects_non_bytes_transaction() -> None:
    with pytest.raises(TypeError, match="every transaction"):
        Block.create(("invalid",), ZERO_HASH, timestamp=100)  # type: ignore[arg-type]


def test_header_is_immutable() -> None:
    header = BlockHeader(1, 100, ZERO_HASH, ZERO_HASH)

    with pytest.raises(FrozenInstanceError):
        header.nonce = 10  # type: ignore[misc]


@pytest.mark.parametrize("timestamp", [-1, True, 1.5])
def test_header_rejects_invalid_timestamp(timestamp: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        BlockHeader(1, timestamp, ZERO_HASH, ZERO_HASH)  # type: ignore[arg-type]


def test_header_rejects_invalid_hash() -> None:
    with pytest.raises(ValueError, match="previous_hash"):
        BlockHeader(1, 100, "invalid", ZERO_HASH)


@pytest.mark.parametrize("value", [0, -1, True, 1.5])
def test_header_rejects_invalid_version(value: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        BlockHeader(value, 100, ZERO_HASH, ZERO_HASH)  # type: ignore[arg-type]


@pytest.mark.parametrize("value", [-1, True, 1.5])
def test_header_rejects_invalid_nonce(value: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        BlockHeader(1, 100, ZERO_HASH, ZERO_HASH, value)  # type: ignore[arg-type]


def test_block_create_rejects_invalid_transaction_collection() -> None:
    with pytest.raises(TypeError, match="tuple or list"):
        Block.create("invalid", ZERO_HASH, timestamp=100)  # type: ignore[arg-type]
