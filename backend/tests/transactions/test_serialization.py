"""Tests for deterministic transaction serialization."""

import json

import pytest
from pycoin.crypto.keys import generate_keypair
from pycoin.transactions.exceptions import InvalidTransactionError
from pycoin.transactions.serialization import (
    deserialize_transaction,
    serialize_transaction,
    serialize_unsigned_transaction,
    transaction_from_dict,
    transaction_to_dict,
)
from pycoin.transactions.transaction_inputs import TransactionInput
from pycoin.transactions.transaction_outputs import TransactionOutput
from pycoin.transactions.transactions import Transaction


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
                unlocking_data=b"sample-signature",
            )
        ],
        outputs=[
            TransactionOutput(
                amount=500,
                recipient_public_key=public_key,
            )
        ],
    )


def test_transaction_serialization_is_deterministic(sample_transaction):
    first = serialize_transaction(sample_transaction)
    second = serialize_transaction(sample_transaction)

    assert first == second


def test_transaction_serialization_round_trip(sample_transaction):
    serialized = serialize_transaction(sample_transaction)
    restored = deserialize_transaction(serialized)

    assert restored == sample_transaction


def test_transaction_serialization_is_valid_json(sample_transaction):
    serialized = serialize_transaction(sample_transaction)

    data = json.loads(serialized)

    assert data["format"] == "PyCoin:Transaction"
    assert data["format_version"] == 1
    assert data["version"] == sample_transaction.version


def test_binary_fields_use_hexadecimal(sample_transaction):
    data = transaction_to_dict(sample_transaction)

    assert (
        data["inputs"][0]["unlocking_data"]
        == sample_transaction.inputs[0].unlocking_data.hex()
    )
    assert (
        data["outputs"][0]["recipient_public_key"]
        == sample_transaction.outputs[0].recipient_public_key.hex()
    )


def test_unsigned_serialization_excludes_unlocking_data(sample_transaction):
    data = json.loads(serialize_unsigned_transaction(sample_transaction))

    assert "unlocking_data" not in data["inputs"][0]


def test_unsigned_serialization_is_independent_of_unlocking_data(sample_transaction):
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

    assert serialize_unsigned_transaction(sample_transaction) == (
        serialize_unsigned_transaction(changed_transaction)
    )


def test_full_serialization_changes_with_unlocking_data(sample_transaction):
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

    assert serialize_transaction(sample_transaction) != (
        serialize_transaction(changed_transaction)
    )


def test_non_transaction_serialization_input_rejected():
    with pytest.raises(TypeError):
        serialize_transaction("invalid")


def test_non_bytes_deserialization_input_rejected():
    with pytest.raises(TypeError):
        deserialize_transaction("not bytes")


@pytest.mark.parametrize(
    "serialized",
    [
        b"",
        b"{invalid json}",
        b"\xff",
        b"[]",
        b"null",
        b'"string"',
    ],
)
def test_invalid_json_rejected(serialized):
    with pytest.raises(InvalidTransactionError):
        deserialize_transaction(serialized)


def test_duplicate_json_keys_rejected():
    serialized = (
        b'{"format":"PyCoin:Transaction","format":"PyCoin:Transaction",'
        b'"format_version":1,"version":1,"lock_time":0,'
        b'"inputs":[],"outputs":[]}'
    )

    with pytest.raises(InvalidTransactionError, match="duplicate JSON key"):
        deserialize_transaction(serialized)


def test_unsupported_format_rejected(sample_transaction):
    data = transaction_to_dict(sample_transaction)
    data["format"] = "Unknown"

    with pytest.raises(InvalidTransactionError, match="unsupported transaction format"):
        transaction_from_dict(data)


def test_unsupported_format_version_rejected(sample_transaction):
    data = transaction_to_dict(sample_transaction)
    data["format_version"] = 99

    with pytest.raises(
        InvalidTransactionError, match="unsupported transaction format version"
    ):
        transaction_from_dict(data)


def test_missing_top_level_field_rejected(sample_transaction):
    data = transaction_to_dict(sample_transaction)
    del data["lock_time"]

    with pytest.raises(InvalidTransactionError, match="invalid fields"):
        transaction_from_dict(data)


def test_unexpected_top_level_field_rejected(sample_transaction):
    data = transaction_to_dict(sample_transaction)
    data["unexpected"] = True

    with pytest.raises(InvalidTransactionError, match="invalid fields"):
        transaction_from_dict(data)


def test_invalid_unlocking_data_hex_rejected(sample_transaction):
    data = transaction_to_dict(sample_transaction)
    data["inputs"][0]["unlocking_data"] = "not-hex"

    with pytest.raises(InvalidTransactionError, match="invalid hexadecimal"):
        transaction_from_dict(data)


def test_uppercase_hex_rejected(sample_transaction):
    data = transaction_to_dict(sample_transaction)
    data["outputs"][0]["recipient_public_key"] = data["outputs"][0][
        "recipient_public_key"
    ].upper()

    with pytest.raises(InvalidTransactionError, match="lowercase hexadecimal"):
        transaction_from_dict(data)


def test_invalid_public_key_rejected(sample_transaction):
    data = transaction_to_dict(sample_transaction)
    data["outputs"][0]["recipient_public_key"] = (b"\x00" * 32).hex()

    with pytest.raises(InvalidTransactionError):
        transaction_from_dict(data)


def test_unknown_input_field_rejected(sample_transaction):
    data = transaction_to_dict(sample_transaction)
    data["inputs"][0]["unexpected"] = "value"

    with pytest.raises(InvalidTransactionError, match="invalid fields"):
        transaction_from_dict(data)


def test_unknown_output_field_rejected(sample_transaction):
    data = transaction_to_dict(sample_transaction)
    data["outputs"][0]["unexpected"] = "value"

    with pytest.raises(InvalidTransactionError, match="invalid fields"):
        transaction_from_dict(data)


def test_serialization_functions_are_exported_from_package():
    from pycoin.transactions import (
        deserialize_transaction,
        serialize_transaction,
        serialize_unsigned_transaction,
        transaction_from_dict,
        transaction_to_dict,
    )

    assert callable(deserialize_transaction)
    assert callable(serialize_transaction)
    assert callable(serialize_unsigned_transaction)
    assert callable(transaction_from_dict)
    assert callable(transaction_to_dict)
