"""Deterministic serialization for PyCoin transactions."""

import json
from typing import Any

from pycoin.core.serialization import canonical_json_bytes
from pycoin.transactions.exceptions import InvalidTransactionError
from pycoin.transactions.transaction_inputs import TransactionInput
from pycoin.transactions.transaction_outputs import TransactionOutput
from pycoin.transactions.transactions import Transaction

TRANSACTION_FORMAT = "PyCoin:Transaction"
TRANSACTION_FORMAT_VERSION = 1

_TOP_LEVEL_FIELDS = {
    "format",
    "format_version",
    "version",
    "lock_time",
    "inputs",
    "outputs",
}
_INPUT_FIELDS = {
    "previous_transaction_id",
    "previous_output_index",
    "unlocking_data",
}
_UNSIGNED_INPUT_FIELDS = {
    "previous_transaction_id",
    "previous_output_index",
}
_OUTPUT_FIELDS = {"amount", "recipient_public_key"}


def _encode_input(
    transaction_input: TransactionInput,
    *,
    include_unlocking_data: bool,
) -> dict[str, Any]:
    """Convert an input into its deterministic JSON representation."""
    result: dict[str, Any] = {
        "previous_transaction_id": transaction_input.previous_transaction_id,
        "previous_output_index": transaction_input.previous_output_index,
    }

    if include_unlocking_data:
        result["unlocking_data"] = transaction_input.unlocking_data.hex()

    return result


def _encode_output(transaction_output: TransactionOutput) -> dict[str, Any]:
    """Convert an output into its deterministic JSON representation."""
    return {
        "amount": transaction_output.amount,
        "recipient_public_key": transaction_output.recipient_public_key.hex(),
    }


def transaction_to_dict(
    transaction: Transaction,
    *,
    include_unlocking_data: bool = True,
) -> dict[str, Any]:
    """Return the versioned dictionary representation of a transaction."""
    if not isinstance(transaction, Transaction):
        raise TypeError("transaction must be a Transaction instance")

    if not isinstance(include_unlocking_data, bool):
        raise TypeError("include_unlocking_data must be a boolean")

    return {
        "format": TRANSACTION_FORMAT,
        "format_version": TRANSACTION_FORMAT_VERSION,
        "version": transaction.version,
        "lock_time": transaction.lock_time,
        "inputs": [
            _encode_input(
                item,
                include_unlocking_data=include_unlocking_data,
            )
            for item in transaction.inputs
        ],
        "outputs": [_encode_output(item) for item in transaction.outputs],
    }


def serialize_transaction(transaction: Transaction) -> bytes:
    """Serialize a transaction, including input unlocking data."""
    return canonical_json_bytes(transaction_to_dict(transaction))


def serialize_unsigned_transaction(transaction: Transaction) -> bytes:
    """Serialize a transaction without input unlocking data."""
    return canonical_json_bytes(
        transaction_to_dict(transaction, include_unlocking_data=False)
    )


def _reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Reject duplicate keys rather than silently accepting the last value."""
    result: dict[str, Any] = {}

    for key, value in pairs:
        if key in result:
            raise InvalidTransactionError(f"duplicate JSON key: {key!r}")
        result[key] = value

    return result


def _decode_hex(value: Any, field_name: str) -> bytes:
    """Decode a strict lowercase hexadecimal field."""
    if not isinstance(value, str):
        raise InvalidTransactionError(f"{field_name} must be a hexadecimal string")

    try:
        decoded = bytes.fromhex(value)
    except ValueError as exc:
        raise InvalidTransactionError(
            f"{field_name} contains invalid hexadecimal data"
        ) from exc

    if decoded.hex() != value:
        raise InvalidTransactionError(
            f"{field_name} must use lowercase hexadecimal without whitespace"
        )

    return decoded


def _require_exact_fields(
    value: dict[str, Any],
    expected: set[str],
    field_name: str,
) -> None:
    """Require an exact field set."""
    actual = set(value)

    if actual != expected:
        missing = sorted(expected - actual)
        unexpected = sorted(actual - expected)

        raise InvalidTransactionError(
            f"{field_name} has invalid fields "
            f"(missing={missing}, unexpected={unexpected})"
        )


def transaction_from_dict(data: dict[str, Any]) -> Transaction:
    """Build a validated transaction from its dictionary representation."""
    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")

    _require_exact_fields(data, _TOP_LEVEL_FIELDS, "transaction")

    if data["format"] != TRANSACTION_FORMAT:
        raise InvalidTransactionError("unsupported transaction format")

    if (
        isinstance(data["format_version"], bool)
        or not isinstance(data["format_version"], int)
        or data["format_version"] != TRANSACTION_FORMAT_VERSION
    ):
        raise InvalidTransactionError("unsupported transaction format version")

    if not isinstance(data["inputs"], list):
        raise InvalidTransactionError("inputs must be a list")

    if not isinstance(data["outputs"], list):
        raise InvalidTransactionError("outputs must be a list")

    inputs: list[TransactionInput] = []

    for index, item in enumerate(data["inputs"]):
        if not isinstance(item, dict):
            raise InvalidTransactionError(f"inputs[{index}] must be an object")

        _require_exact_fields(item, _INPUT_FIELDS, f"inputs[{index}]")

        inputs.append(
            TransactionInput(
                previous_transaction_id=item["previous_transaction_id"],
                previous_output_index=item["previous_output_index"],
                unlocking_data=_decode_hex(
                    item["unlocking_data"],
                    f"inputs[{index}].unlocking_data",
                ),
            )
        )

    outputs: list[TransactionOutput] = []

    for index, item in enumerate(data["outputs"]):
        if not isinstance(item, dict):
            raise InvalidTransactionError(f"outputs[{index}] must be an object")

        _require_exact_fields(item, _OUTPUT_FIELDS, f"outputs[{index}]")

        outputs.append(
            TransactionOutput(
                amount=item["amount"],
                recipient_public_key=_decode_hex(
                    item["recipient_public_key"],
                    f"outputs[{index}].recipient_public_key",
                ),
            )
        )

    return Transaction(
        version=data["version"],
        lock_time=data["lock_time"],
        inputs=inputs,
        outputs=outputs,
    )


def deserialize_transaction(serialized: bytes) -> Transaction:
    """Deserialize JSON bytes into a validated transaction."""
    if not isinstance(serialized, bytes):
        raise TypeError("serialized must be bytes")

    try:
        text = serialized.decode("utf-8")
        data = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_json_keys,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise InvalidTransactionError("invalid transaction JSON") from exc

    if not isinstance(data, dict):
        raise InvalidTransactionError("transaction JSON must contain an object")

    return transaction_from_dict(data)
