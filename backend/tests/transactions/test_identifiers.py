"""Tests for deterministic PyCoin transaction identifiers."""

import re

import pytest
from pycoin.crypto.keys import generate_keypair
from pycoin.transactions import (
    Transaction,
    TransactionInput,
    TransactionOutput,
    calculate_transaction_id,
)


@pytest.fixture
def sample_transaction() -> Transaction:
    _, public_key = generate_keypair()

    return Transaction(
        version=1,
        lock_time=0,
        inputs=[
            TransactionInput(
                previous_transaction_id="a" * 64,
                previous_output_index=1,
                unlocking_data=b"first-signature",
            )
        ],
        outputs=[
            TransactionOutput(
                amount=500,
                recipient_public_key=public_key,
            )
        ],
    )


def test_transaction_id_is_deterministic(sample_transaction):
    first = calculate_transaction_id(sample_transaction)
    second = calculate_transaction_id(sample_transaction)

    assert first == second


def test_transaction_id_is_independent_of_unlocking_data(sample_transaction):
    original_input = sample_transaction.inputs[0]

    changed_transaction = Transaction(
        version=sample_transaction.version,
        lock_time=sample_transaction.lock_time,
        inputs=[
            TransactionInput(
                previous_transaction_id=original_input.previous_transaction_id,
                previous_output_index=original_input.previous_output_index,
                unlocking_data=b"different-signature",
            )
        ],
        outputs=sample_transaction.outputs,
    )

    assert calculate_transaction_id(sample_transaction) == (
        calculate_transaction_id(changed_transaction)
    )


def test_transaction_id_has_64_lowercase_hexadecimal_characters(
    sample_transaction,
):
    transaction_id = calculate_transaction_id(sample_transaction)

    assert len(transaction_id) == 64
    assert re.fullmatch(r"[0-9a-f]{64}", transaction_id)


def test_transaction_id_changes_when_previous_transaction_id_changes(
    sample_transaction,
):
    original_input = sample_transaction.inputs[0]

    changed_transaction = Transaction(
        version=sample_transaction.version,
        lock_time=sample_transaction.lock_time,
        inputs=[
            TransactionInput(
                previous_transaction_id="b" * 64,
                previous_output_index=original_input.previous_output_index,
                unlocking_data=original_input.unlocking_data,
            )
        ],
        outputs=sample_transaction.outputs,
    )

    assert calculate_transaction_id(sample_transaction) != (
        calculate_transaction_id(changed_transaction)
    )


def test_transaction_id_changes_when_previous_output_index_changes(
    sample_transaction,
):
    original_input = sample_transaction.inputs[0]

    changed_transaction = Transaction(
        version=sample_transaction.version,
        lock_time=sample_transaction.lock_time,
        inputs=[
            TransactionInput(
                previous_transaction_id=original_input.previous_transaction_id,
                previous_output_index=original_input.previous_output_index + 1,
                unlocking_data=original_input.unlocking_data,
            )
        ],
        outputs=sample_transaction.outputs,
    )

    assert calculate_transaction_id(sample_transaction) != (
        calculate_transaction_id(changed_transaction)
    )


def test_transaction_id_changes_when_output_amount_changes(sample_transaction):
    original_output = sample_transaction.outputs[0]

    changed_transaction = Transaction(
        version=sample_transaction.version,
        lock_time=sample_transaction.lock_time,
        inputs=sample_transaction.inputs,
        outputs=[
            TransactionOutput(
                amount=original_output.amount + 1,
                recipient_public_key=original_output.recipient_public_key,
            )
        ],
    )

    assert calculate_transaction_id(sample_transaction) != (
        calculate_transaction_id(changed_transaction)
    )


def test_transaction_id_changes_when_recipient_public_key_changes(
    sample_transaction,
):
    _, different_public_key = generate_keypair()
    original_output = sample_transaction.outputs[0]

    changed_transaction = Transaction(
        version=sample_transaction.version,
        lock_time=sample_transaction.lock_time,
        inputs=sample_transaction.inputs,
        outputs=[
            TransactionOutput(
                amount=original_output.amount,
                recipient_public_key=different_public_key,
            )
        ],
    )

    assert calculate_transaction_id(sample_transaction) != (
        calculate_transaction_id(changed_transaction)
    )


def test_transaction_id_changes_when_version_changes(sample_transaction):
    changed_transaction = Transaction(
        version=sample_transaction.version + 1,
        lock_time=sample_transaction.lock_time,
        inputs=sample_transaction.inputs,
        outputs=sample_transaction.outputs,
    )

    assert calculate_transaction_id(sample_transaction) != (
        calculate_transaction_id(changed_transaction)
    )


def test_transaction_id_changes_when_lock_time_changes(sample_transaction):
    changed_transaction = Transaction(
        version=sample_transaction.version,
        lock_time=sample_transaction.lock_time + 1,
        inputs=sample_transaction.inputs,
        outputs=sample_transaction.outputs,
    )

    assert calculate_transaction_id(sample_transaction) != (
        calculate_transaction_id(changed_transaction)
    )


def test_non_transaction_input_is_rejected():
    with pytest.raises(TypeError, match="transaction must be a Transaction"):
        calculate_transaction_id("invalid")
