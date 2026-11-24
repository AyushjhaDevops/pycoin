"""Immutable PyCoin transaction model."""

from dataclasses import dataclass

from pycoin.transactions.exceptions import InvalidTransactionError
from pycoin.transactions.transaction_inputs import TransactionInput
from pycoin.transactions.transaction_outputs import TransactionOutput


@dataclass(frozen=True, slots=True)
class Transaction:
    """Represent a transaction spending previous outputs and creating new ones."""

    version: int
    inputs: tuple[TransactionInput, ...] | list[TransactionInput]
    outputs: tuple[TransactionOutput, ...] | list[TransactionOutput]
    lock_time: int = 0

    def __post_init__(self) -> None:
        if isinstance(self.version, bool) or not isinstance(self.version, int):
            raise TypeError("version must be an integer")

        if self.version <= 0:
            raise InvalidTransactionError("version must be greater than zero")

        if isinstance(self.lock_time, bool) or not isinstance(self.lock_time, int):
            raise TypeError("lock_time must be an integer")

        if self.lock_time < 0:
            raise InvalidTransactionError("lock_time cannot be negative")

        if not isinstance(self.inputs, (list, tuple)):
            raise TypeError("inputs must be a list or tuple")

        if not isinstance(self.outputs, (list, tuple)):
            raise TypeError("outputs must be a list or tuple")

        normalized_inputs = tuple(self.inputs)
        normalized_outputs = tuple(self.outputs)

        if not normalized_inputs:
            raise InvalidTransactionError("transaction must contain at least one input")

        if not normalized_outputs:
            raise InvalidTransactionError(
                "transaction must contain at least one output"
            )

        if not all(isinstance(item, TransactionInput) for item in normalized_inputs):
            raise TypeError("all inputs must be TransactionInput instances")

        if not all(isinstance(item, TransactionOutput) for item in normalized_outputs):
            raise TypeError("all outputs must be TransactionOutput instances")

        outpoints = [
            (item.previous_transaction_id, item.previous_output_index)
            for item in normalized_inputs
        ]

        if len(outpoints) != len(set(outpoints)):
            raise InvalidTransactionError(
                "transaction cannot contain duplicate input references"
            )

        object.__setattr__(self, "inputs", normalized_inputs)
        object.__setattr__(self, "outputs", normalized_outputs)
