"""Tests for the PyCoin blockchain."""

import pytest
from pycoin.core.blockchain import Blockchain, create_genesis_block
from pycoin.core.blocks import Block


def test_genesis_block_is_deterministic() -> None:
    first = create_genesis_block()
    second = create_genesis_block()

    assert first == second
    assert first.header.timestamp == 0
    assert first.header.previous_hash == "0" * 64


def test_new_block_can_be_added() -> None:
    chain = Blockchain()
    genesis = chain.latest_block

    block = Block.create(
        transactions=(b"tx-1",),
        previous_hash=genesis.hash,
        timestamp=1,
    )

    chain.add_block(block)

    assert len(chain.blocks) == 2
    assert chain.latest_block == block
    assert chain.is_valid()


def test_block_with_wrong_previous_hash_is_rejected() -> None:
    chain = Blockchain()

    block = Block.create(
        transactions=(b"tx-1",),
        previous_hash="1" * 64,
        timestamp=1,
    )

    with pytest.raises(ValueError, match="previous_hash"):
        chain.add_block(block)


def test_block_with_earlier_timestamp_is_rejected() -> None:
    chain = Blockchain()

    first = Block.create(
        transactions=(b"tx-1",),
        previous_hash=chain.latest_block.hash,
        timestamp=10,
    )
    chain.add_block(first)

    earlier = Block.create(
        transactions=(b"tx-2",),
        previous_hash=first.hash,
        timestamp=9,
    )

    with pytest.raises(ValueError, match="timestamp"):
        chain.add_block(earlier)


def test_chain_rejects_wrong_genesis_block() -> None:
    fake_genesis = Block.create(
        transactions=(b"fake",),
        previous_hash="0" * 64,
        timestamp=0,
    )

    assert not Blockchain.validate_chain((fake_genesis,))


def test_chain_rejects_empty_sequence() -> None:
    assert not Blockchain.validate_chain(())


def test_blocks_property_returns_tuple() -> None:
    chain = Blockchain()

    assert isinstance(chain.blocks, tuple)


def test_non_block_object_is_rejected() -> None:
    chain = Blockchain()

    with pytest.raises(TypeError, match="block must be a Block"):
        chain.add_block("not-a-block")  # type: ignore[arg-type]
