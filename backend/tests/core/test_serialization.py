"""Tests for canonical PyCoin serialization."""

import json

import pytest
from pycoin.core.block_serialization import serialize_block
from pycoin.core.blocks import Block
from pycoin.core.serialization import canonical_json_bytes


def test_canonical_json_ignores_dictionary_insertion_order() -> None:
    first = canonical_json_bytes({"b": 2, "a": 1})
    second = canonical_json_bytes({"a": 1, "b": 2})

    assert first == second


def test_canonical_json_uses_compact_encoding() -> None:
    result = canonical_json_bytes({"a": 1, "b": 2})

    assert result == b'{"a":1,"b":2}'


def test_canonical_json_rejects_non_dictionary() -> None:
    with pytest.raises(TypeError):
        canonical_json_bytes(["not", "a", "dictionary"])  # type: ignore[arg-type]


def test_canonical_json_rejects_non_json_values() -> None:
    with pytest.raises(ValueError):
        canonical_json_bytes({"invalid": object()})


def test_block_serialization_is_deterministic() -> None:
    first = Block.create((b"transaction",), "0" * 64, timestamp=100)
    second = Block.create((b"transaction",), "0" * 64, timestamp=100)

    assert serialize_block(first) == serialize_block(second)


def test_block_serialization_contains_header_and_transactions() -> None:
    block = Block.create((b"hello",), "0" * 64, timestamp=100)

    payload = json.loads(serialize_block(block))

    assert payload["header"]["timestamp"] == 100
    assert payload["transactions"] == ["68656c6c6f"]


def test_block_serialization_rejects_invalid_input() -> None:
    with pytest.raises(TypeError):
        serialize_block("not a block")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "value",
    [float("nan"), float("inf"), float("-inf")],
)
def test_canonical_json_rejects_non_finite_numbers(value: float) -> None:
    with pytest.raises(ValueError):
        canonical_json_bytes({"value": value})
