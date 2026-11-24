"""Immutable UTXO transaction input model."""

import re
from dataclasses import dataclass

from pycoin.transactions.exceptions import InvalidTransactionError

_TRANSACTION_ID_PATTERN = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True, slots=True)
class TransactionInput:
    """Reference a previous transaction output.

    unlocking_data is empty until the input is signed in a later
    transaction-engine subphase.
    """

    previous_transaction_id: str
    previous_output_index: int
    unlocking_data: bytes = b""

    def __post_init__(self) -> None:
        if not isinstance(self.previous_transaction_id, str):
            raise TypeError("previous_transaction_id must be a string")

        if not _TRANSACTION_ID_PATTERN.fullmatch(self.previous_transaction_id):
            raise InvalidTransactionError(
                "previous_transaction_id must be 64 lowercase hexadecimal characters"
            )

        if isinstance(self.previous_output_index, bool) or not isinstance(
            self.previous_output_index, int
        ):
            raise TypeError("previous_output_index must be an integer")

        if self.previous_output_index < 0:
            raise InvalidTransactionError("previous_output_index cannot be negative")

        if not isinstance(self.unlocking_data, bytes):
            raise TypeError("unlocking_data must be bytes")
