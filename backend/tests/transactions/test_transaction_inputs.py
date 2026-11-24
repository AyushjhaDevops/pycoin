"""Tests for PyCoin transaction inputs."""

import pytest
from pycoin.transactions import InvalidTransactionError, TransactionInput

TX_ID = "a" * 64


def test_valid_transaction_input():
    tx_input = TransactionInput(TX_ID, 0)

    assert tx_input.previous_transaction_id == TX_ID
    assert tx_input.previous_output_index == 0
    assert tx_input.unlocking_data == b""


def test_transaction_input_accepts_unlocking_data():
    tx_input = TransactionInput(TX_ID, 1, b"signature")

    assert tx_input.unlocking_data == b"signature"


@pytest.mark.parametrize(
    "tx_id",
    [
        "",
        "a" * 63,
        "a" * 65,
        "A" * 64,
        "g" * 64,
    ],
)
def test_invalid_transaction_id(tx_id):
    with pytest.raises(InvalidTransactionError):
        TransactionInput(tx_id, 0)


def test_transaction_id_must_be_string():
    with pytest.raises(TypeError):
        TransactionInput(None, 0)  # type: ignore[arg-type]


@pytest.mark.parametrize("index", [-1, 1.5, True, "0"])
def test_invalid_output_index(index):
    with pytest.raises((TypeError, InvalidTransactionError)):
        TransactionInput(TX_ID, index)  # type: ignore[arg-type]


def test_unlocking_data_must_be_bytes():
    with pytest.raises(TypeError):
        TransactionInput(TX_ID, 0, "signature")  # type: ignore[arg-type]


def test_transaction_input_is_immutable():
    tx_input = TransactionInput(TX_ID, 0)

    with pytest.raises(AttributeError):
        tx_input.previous_output_index = 1  # type: ignore[misc]
