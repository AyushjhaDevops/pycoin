"""Tests for PyCoin Merkle tree calculations."""

import pytest
from pycoin.core.merkle import merkle_root


def test_empty_merkle_root_is_deterministic() -> None:
    assert merkle_root(()) == merkle_root(())
    assert len(merkle_root(())) == 64


def test_single_transaction_has_stable_root() -> None:
    assert merkle_root((b"transaction-1",)) == merkle_root((b"transaction-1",))


def test_transaction_order_changes_root() -> None:
    first = merkle_root((b"tx-a", b"tx-b"))
    second = merkle_root((b"tx-b", b"tx-a"))

    assert first != second


def test_odd_transaction_count_is_supported() -> None:
    root = merkle_root((b"a", b"b", b"c"))

    assert len(root) == 64


def test_empty_and_nonempty_roots_differ() -> None:
    assert merkle_root(()) != merkle_root((b"transaction",))


def test_invalid_transaction_type_is_rejected() -> None:
    with pytest.raises(TypeError):
        merkle_root((b"valid", "invalid"))  # type: ignore[arg-type]


def test_invalid_collection_type_is_rejected() -> None:
    with pytest.raises(TypeError):
        merkle_root(b"not-a-collection")  # type: ignore[arg-type]


def test_single_transaction_matches_known_root() -> None:
    assert (
        merkle_root((b"transaction-1",))
        == "9d72eb05c9d5f45610d703437df9d449d327b9f9f58cd5eee84db44d95630aac"
    )
