"""Deterministic block serialization for PyCoin."""

from pycoin.core.blocks import Block
from pycoin.core.serialization import canonical_json_bytes


def serialize_block(block: Block) -> bytes:
    """Serialize a block into canonical JSON bytes."""
    if not isinstance(block, Block):
        raise TypeError("block must be a Block")

    payload = {
        "header": block.header.to_dict(),
        "transactions": [transaction.hex() for transaction in block.transactions],
    }

    return canonical_json_bytes(payload)
