"""Tests for PyCoin transaction outputs."""

import pytest
from pycoin.crypto.keys import generate_keypair
from pycoin.transactions import InvalidTransactionError, TransactionOutput


def make_output(amount=100):
    _, public_key = generate_keypair()
    return TransactionOutput(amount, public_key)


def test_valid_transaction_output():
    output = make_output()

    assert output.amount == 100
    assert len(output.recipient_public_key) == 32


def test_recipient_address_uses_existing_address_format():
    output = make_output()

    assert output.recipient_address.startswith("PYC1")
    assert len(output.recipient_address) == 44


@pytest.mark.parametrize("amount", [0, -1, -100])
def test_non_positive_amount_rejected(amount):
    _, public_key = generate_keypair()

    with pytest.raises(InvalidTransactionError):
        TransactionOutput(amount, public_key)


@pytest.mark.parametrize("amount", [1.5, "100", True])
def test_non_integer_amount_rejected(amount):
    _, public_key = generate_keypair()

    with pytest.raises(TypeError):
        TransactionOutput(amount, public_key)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "public_key",
    [
        b"",
        b"short",
        b"x" * 31,
        b"x" * 33,
    ],
)
def test_invalid_public_key_length_rejected(public_key):
    with pytest.raises(InvalidTransactionError):
        TransactionOutput(100, public_key)


def test_public_key_must_be_bytes():
    with pytest.raises(TypeError):
        TransactionOutput(100, "not-a-key")  # type: ignore[arg-type]


def test_transaction_output_is_immutable():
    output = make_output()

    with pytest.raises(AttributeError):
        output.amount = 200  # type: ignore[misc]


@pytest.mark.parametrize(
    "public_key",
    [
        b"\x00" * 32,
        b"x" * 32,
    ],
)
def test_invalid_ed25519_public_key_rejected(public_key):
    with pytest.raises(
        InvalidTransactionError,
        match="valid Ed25519 public key",
    ):
        TransactionOutput(100, public_key)
