"""Blockchain and genesis-block implementation for PyCoin."""

from pycoin.core.blocks import Block
from pycoin.core.merkle import merkle_root

GENESIS_PREVIOUS_HASH = "0" * 64
GENESIS_TIMESTAMP = 0


def create_genesis_block() -> Block:
    """Create the deterministic first block in the PyCoin chain."""
    return Block.create(
        transactions=(),
        previous_hash=GENESIS_PREVIOUS_HASH,
        timestamp=GENESIS_TIMESTAMP,
        version=1,
        nonce=0,
    )


class Blockchain:
    """In-memory blockchain with structural and link validation."""

    def __init__(self) -> None:
        self._blocks: list[Block] = [create_genesis_block()]

    @property
    def blocks(self) -> tuple[Block, ...]:
        """Return an immutable snapshot of the current chain."""
        return tuple(self._blocks)

    @property
    def latest_block(self) -> Block:
        """Return the most recently appended block."""
        return self._blocks[-1]

    def add_block(self, block: Block) -> None:
        """Validate and append a block to the chain."""
        if not isinstance(block, Block):
            raise TypeError("block must be a Block")

        previous = self.latest_block

        if block.header.previous_hash != previous.hash:
            raise ValueError("block previous_hash does not match chain tip")

        if block.header.timestamp < previous.header.timestamp:
            raise ValueError("block timestamp cannot precede previous block")

        if block.header.merkle_root != merkle_root(block.transactions):
            raise ValueError("block Merkle root is invalid")

        self._blocks.append(block)

    @staticmethod
    def validate_chain(blocks: tuple[Block, ...] | list[Block]) -> bool:
        """Check genesis identity, block integrity, and hash links."""
        if not isinstance(blocks, (tuple, list)) or not blocks:
            return False

        if any(not isinstance(block, Block) for block in blocks):
            return False

        if blocks[0] != create_genesis_block():
            return False

        for index in range(1, len(blocks)):
            previous = blocks[index - 1]
            current = blocks[index]

            if current.header.previous_hash != previous.hash:
                return False

            if current.header.timestamp < previous.header.timestamp:
                return False

            if current.header.merkle_root != merkle_root(current.transactions):
                return False

        return True

    def is_valid(self) -> bool:
        """Validate the current blockchain."""
        return self.validate_chain(self._blocks)
