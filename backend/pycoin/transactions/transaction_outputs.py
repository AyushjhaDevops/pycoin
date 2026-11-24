"""Immutable UTXO transaction output model."""

from dataclasses import dataclass

from nacl.bindings import crypto_core_ed25519_is_valid_point

from pycoin.crypto.addresses import derive_address
from pycoin.crypto.keys import PUBLIC_KEY_SIZE
from pycoin.transactions.exceptions import InvalidTransactionError


@dataclass(frozen=True, slots=True)
class TransactionOutput:
    """Lock an integer amount of PYC to an Ed25519 public key."""

    amount: int
    recipient_public_key: bytes

    def __post_init__(self) -> None:
        if isinstance(self.amount, bool) or not isinstance(self.amount, int):
            raise TypeError("amount must be an integer")

        if self.amount <= 0:
            raise InvalidTransactionError("amount must be greater than zero")

        if not isinstance(self.recipient_public_key, bytes):
            raise TypeError("recipient_public_key must be bytes")

        if len(self.recipient_public_key) != PUBLIC_KEY_SIZE:
            raise InvalidTransactionError(
                f"recipient_public_key must be {PUBLIC_KEY_SIZE} bytes"
            )

        if not crypto_core_ed25519_is_valid_point(self.recipient_public_key):
            raise InvalidTransactionError(
                "recipient_public_key must be a valid Ed25519 public key"
            )

    @property
    def recipient_address(self) -> str:
        """Return the existing versioned PyCoin address for this key."""
        return derive_address(self.recipient_public_key)
