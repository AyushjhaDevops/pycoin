"""Tests for the PyCoin transaction model."""

import pytest
from pycoin.crypto.keys import generate_keypair
from pycoin.transactions import (
    InvalidTransactionError,
    Transaction,
    TransactionInput,
    TransactionOutput,
)

TX_ID_A = "a" * 64
TX_ID_B = "b" * 64


def make_input(tx_id=TX_ID_A, index=0):
    return TransactionInput(tx_id, index)


def make_output(amount=100):
    _, public_key = generate_keypair()
    return TransactionOutput(amount, public_key)


def make_transaction(inputs=None, outputs=None):
    return Transaction(
        version=1,
        inputs=inputs if inputs is not None else [make_input()],
        outputs=outputs if outputs is not None else [make_output()],
    )


def test_valid_transaction():
    transaction = make_transaction()

    assert transaction.version == 1
    assert len(transaction.inputs) == 1
    assert len(transaction.outputs) == 1
    assert transaction.lock_time == 0


def test_custom_lock_time():
    transaction = Transaction(
        1,
        [make_input()],
        [make_output()],
        lock_time=500,
    )

    assert transaction.lock_time == 500


def test_list_collections_are_normalized_to_tuples():
    inputs = [make_input()]
    outputs = [make_output()]

    transaction = Transaction(1, inputs, outputs)

    assert isinstance(transaction.inputs, tuple)
    assert isinstance(transaction.outputs, tuple)


def test_empty_inputs_rejected():
    with pytest.raises(InvalidTransactionError):
        make_transaction(inputs=[])


def test_empty_outputs_rejected():
    with pytest.raises(InvalidTransactionError):
        make_transaction(outputs=[])


@pytest.mark.parametrize("version", [0, -1])
def test_invalid_version_rejected(version):
    with pytest.raises(InvalidTransactionError):
        Transaction(version, [make_input()], [make_output()])


def test_version_must_be_integer():
    with pytest.raises(TypeError):
        Transaction("1", [make_input()], [make_output()])  # type: ignore[arg-type]


@pytest.mark.parametrize("lock_time", [-1, 1.5, True])
def test_invalid_lock_time_rejected(lock_time):
    with pytest.raises((TypeError, InvalidTransactionError)):
        Transaction(
            1,
            [make_input()],
            [make_output()],
            lock_time=lock_time,
        )  # type: ignore[arg-type]


def test_invalid_input_collection_type():
    with pytest.raises(TypeError):
        Transaction(1, "invalid", [make_output()])  # type: ignore[arg-type]


def test_invalid_output_collection_type():
    with pytest.raises(TypeError):
        Transaction(1, [make_input()], "invalid")  # type: ignore[arg-type]


def test_invalid_input_member_rejected():
    with pytest.raises(TypeError):
        Transaction(1, [object()], [make_output()])  # type: ignore[list-item]


def test_invalid_output_member_rejected():
    with pytest.raises(TypeError):
        Transaction(1, [make_input()], [object()])  # type: ignore[list-item]


def test_duplicate_input_reference_rejected():
    duplicate_a = make_input(TX_ID_A, 0)
    duplicate_b = make_input(TX_ID_A, 0)

    with pytest.raises(InvalidTransactionError):
        make_transaction(inputs=[duplicate_a, duplicate_b])


def test_distinct_output_indexes_are_allowed():
    transaction = make_transaction(
        inputs=[
            make_input(TX_ID_A, 0),
            make_input(TX_ID_A, 1),
            make_input(TX_ID_B, 0),
        ]
    )

    assert len(transaction.inputs) == 3


def test_transaction_is_immutable():
    transaction = make_transaction()

    with pytest.raises(AttributeError):
        transaction.version = 2  # type: ignore[misc]


def test_transaction_collections_are_immutable():
    transaction = make_transaction()

    with pytest.raises(AttributeError):
        transaction.inputs = ()  # type: ignore[misc]
